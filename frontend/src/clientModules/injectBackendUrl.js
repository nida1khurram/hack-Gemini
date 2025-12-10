// Client module to inject BACKEND_URL as a global variable
// This will be executed when the Docusaurus app starts in the browser

// This module will run in the browser and can access Docusaurus site config
// The proper way is to create a global variable that the API service can use
if (typeof window !== 'undefined') {
  // Since process.env is not available in the browser, we'll use a fixed value for development
  // In production, this would need to be configured differently
  window.BACKEND_URL = 'http://localhost:8000';
  console.log('Backend URL set to:', window.BACKEND_URL);
}