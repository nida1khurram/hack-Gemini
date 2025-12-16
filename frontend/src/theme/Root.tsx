// frontend/src/theme/Root.tsx

import React from 'react';
import { SessionProvider } from 'next-auth/react';

// Default implementation, that you can customize
function Root({children}) {
  return (
    <SessionProvider>
      {children}
    </SessionProvider>
  );
}

export default Root;
