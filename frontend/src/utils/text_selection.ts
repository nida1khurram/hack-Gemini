// frontend/src/utils/text_selection.ts

export function getSelectedText(): string | null {
  if (typeof window === 'undefined') {
    return null;
  }
  const selection = window.getSelection();
  if (selection && selection.rangeCount > 0) {
    return selection.toString().trim();
  }
  return null;
}

export function getSelectionCoordinates(): { x: number; y: number } | null {
  if (typeof window === 'undefined') {
    return null;
  }
  const selection = window.getSelection();
  if (selection && selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    if (rect.x === 0 && rect.y === 0) { // No actual selection or off-screen
      return null;
    }
    return { x: rect.right + window.scrollX, y: rect.bottom + window.scrollY };
  }
  return null;
}
