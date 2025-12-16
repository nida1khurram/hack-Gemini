// nodejs_backend/src/index.ts

import express from 'express';
import { auth } from './auth'; // Import Auth.js setup
import cookieParser from 'cookie-parser'; // For parsing cookies
import jwt from 'jsonwebtoken'; // For JWT verification

const app = express();
const PORT = process.env.PORT || 3001; // Use a different port than frontend

app.use(express.json());
app.use(cookieParser());

// Auth.js route handler
app.all('/api/auth/*', async (req, res) => {
  await auth(req, res);
});

// Extend Request type to include user property
declare global {
  namespace Express {
    interface Request {
      user?: { id: string; email: string; name?: string };
    }
  }
}

// Middleware to protect routes by verifying JWT from cookie
const isAuthenticated = (req: express.Request, res: express.Response, next: express.NextFunction) => {
  const token = req.cookies['next-auth.session-token']; // Auth.js stores JWT in this cookie
  
  if (!token) {
    return res.status(401).send('Unauthorized: No session token found');
  }

  try {
    const decoded = jwt.verify(token, process.env.AUTH_SECRET as string) as { id: string; email: string; name?: string };
    req.user = decoded; // Attach decoded user payload to request
    next();
  } catch (err) {
    console.error('JWT verification failed:', err);
    return res.status(401).send('Unauthorized: Invalid session token');
  }
};


app.get('/', (req, res) => {
  res.send('Node.js Backend is running!');
});

app.get('/api/protected', isAuthenticated, (req, res) => {
  res.send(`This is a protected route. Welcome, ${req.user?.name || req.user?.email}!`);
});

app.listen(PORT, () => {
  console.log(`Node.js Backend running on http://localhost:${PORT}`);
});
