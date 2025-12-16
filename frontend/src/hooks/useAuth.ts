import { useSession, signIn, signOut } from 'next-auth/react';

interface AuthState {
  isAuthenticated: boolean;
  user: {
    id?: string; // Auth.js session user might have an id
    name?: string;
    email?: string;
    image?: string;
    // Add other relevant properties from Auth.js session.user if needed
  } | null;
  loading: boolean;
  error: string | null; // Auth.js handles errors internally, so this might be less used
  login: (email, password) => Promise<any>; // signIn returns a Promise<void | undefined | SignInResponse>
  register: (email, password, username) => Promise<any>;
  logout: () => Promise<any>; // signOut returns Promise<undefined | string>
}

const useAuth = (): AuthState => {
  const { data: session, status } = useSession(); // Auth.js hook

  const isAuthenticated = status === 'authenticated';
  const loading = status === 'loading';
  const user = session?.user || null;

  const login = async (email, password) => {
    const result = await signIn('credentials', {
      redirect: false, // Prevent redirect
      email,
      password,
    });
    if (result?.error) {
      throw new Error(result.error);
    }
    return result;
  };

  const register = async (email, password, username) => {
    // Auth.js doesn't have a built-in register function.
    // This will need a custom API endpoint in the Node.js backend.
    // For now, this is a placeholder.
    console.warn("Custom registration endpoint not yet implemented in Node.js backend.");
    throw new Error("Custom registration not implemented yet.");
  };

  const logout = async () => {
    // Sign out from Auth.js
    await signOut({ redirect: false });
  };

  return {
    isAuthenticated,
    user,
    loading,
    error: null, // Auth.js handles errors in signIn/signOut return, or through session status
    login,
    register,
    logout,
  };
};

export default useAuth;
