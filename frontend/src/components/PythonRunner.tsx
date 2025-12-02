import React, { useState, useEffect, useRef, useCallback } from 'react';
import CodeEditor from '@uiw/react-textarea-code-editor';

interface PyodideResult {
  output: string;
  error: string;
}

// Custom hook to load and manage Pyodide
function usePyodide() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const pyodideRef = useRef<any>(null); // Ref to store the pyodide instance

  useEffect(() => {
    const load = async () => {
      try {
        // @ts-ignore - pyodide is loaded globally by the script
        // Check if loadPyodide is already available (e.g., from a previous component instance)
        if (!window.loadPyodide) {
          // Dynamically add the Pyodide script if not already present
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js'; // Use v0.25.0
          script.onload = async () => {
            // @ts-ignore
            pyodideRef.current = await window.loadPyodide();
            setIsLoading(false);
          };
          script.onerror = (e) => {
            console.error("Failed to load Pyodide script:", e);
            setError("Failed to load Pyodide script");
            setIsLoading(false);
          };
          document.head.appendChild(script);
        } else {
          // If loadPyodide is already on window, it means script is loaded or loading
          // @ts-ignore
          pyodideRef.current = await window.loadPyodide();
          setIsLoading(false);
        }
      } catch (err: any) {
        console.error("Error loading Pyodide:", err);
        setError(err.message || "Failed to load Pyodide");
        setIsLoading(false);
      }
    };

    load(); // Call load function

  }, []); // Empty dependency array means this effect runs once on mount

  const runPython = useCallback(async (code: string): Promise<PyodideResult> => {
    if (!pyodideRef.current) {
      return { output: '', error: 'Pyodide not loaded.' };
    }
    let output = '';
    let error = '';

    // Capture stdout and stderr
    const stdoutBuffer: string[] = [];
    const stderrBuffer: string[] = [];

    const originalStdout = pyodideRef.current.globals.get("sys").stdout;
    const originalStderr = pyodideRef.current.globals.get("sys").stderr;

    try {
      // Redirect stdout and stderr to capture
      pyodideRef.current.globals.get("sys").stdout = {
        write: (s: string) => { stdoutBuffer.push(s); }
      };
      pyodideRef.current.globals.get("sys").stderr = {
        write: (s: string) => { stderrBuffer.push(s); }
      };

      await pyodideRef.current.runPythonAsync(code);
    } catch (err: any) {
      // Pyodide can throw Python errors as JS errors
      // console.error("Python execution error:", err);
      // Attempt to get a more structured error from Pyodide's sys.stderr buffer if available
      if (stderrBuffer.length > 0) {
        error += stderrBuffer.join('');
      } else {
        error += err.toString(); // Fallback to JS error string
      }
    } finally {
      // Restore original stdout/stderr
      pyodideRef.current.globals.get("sys").stdout = originalStdout;
      pyodideRef.current.globals.get("sys").stderr = originalStderr;

      output = stdoutBuffer.join('');
      // If there was an error captured by stderrBuffer, prioritize that
      if (stderrBuffer.length > 0 && !error) { // Only set error if not already set by catch
        error = stderrBuffer.join('');
      }
    }
    return { output, error };
  }, []); // runPython depends only on pyodideRef.current which is stable once loaded.

  return { isLoading, error, runPython };
}

interface PythonRunnerProps {
  code: string; // Initial code to display
}

const PythonRunner: React.FC<PythonRunnerProps> = ({ code: initialCode }) => {
  const { isLoading, error, runPython } = usePyodide();
  const [code, setCode] = useState(initialCode);
  const [output, setOutput] = useState('');
  const [runError, setRunError] = useState<string | null>(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const handleRun = async () => {
    setIsExecuting(true);
    setRunError(null);
    setOutput(''); // Clear previous output
    const result = await runPython(code);
    setOutput(result.output);
    if (result.error) {
      setRunError(result.error);
    }
    setIsExecuting(false);
  };

  if (error) {
    return <div style={{ color: 'red', padding: '10px' }}>Error loading Python environment: {error}</div>;
  }

  return (
    <div style={{ margin: '20px 0', border: '1px solid #ddd', borderRadius: '5px', overflow: 'hidden' }}>
      {isLoading ? (
        <div style={{ padding: '10px', backgroundColor: '#f0f0f0' }}>Loading Python environment...</div>
      ) : (
        <>
          <CodeEditor
            value={code}
            language="python"
            placeholder="Write your Python code here"
            onChange={(evn) => setCode(evn.target.value)}
            padding={15}
            style={{
              fontSize: 12,
              backgroundColor: "#f5f5f5",
              fontFamily: 'ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace',
            }}
          />
          <button
            onClick={handleRun}
            disabled={isLoading || isExecuting}
            style={{
              display: 'block',
              width: '100%',
              padding: '10px',
              backgroundColor: '#4B8BBE', // Primary color from user's theme
              color: 'white',
              border: 'none',
              cursor: isLoading || isExecuting ? 'not-allowed' : 'pointer',
              fontSize: '16px',
              fontWeight: 'bold',
            }}
          >
            {isExecuting ? 'Running...' : 'Run Python Code'}
          </button>
          <div style={{ backgroundColor: '#333', color: '#eee', padding: '10px', minHeight: '50px', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            {runError ? <pre style={{ color: 'red', margin: 0 }}>{runError}</pre> : output}
          </div>
        </>
      )}
    </div>
  );
};

export default PythonRunner;
