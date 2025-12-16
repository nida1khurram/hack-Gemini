// nodejs_backend/src/auth.ts

import { Auth } from '@auth/core';
import Google from '@auth/core/providers/google';
import GitHub from '@auth/core/providers/github';
import { PrismaAdapter } from '@auth/prisma-adapter';
import { PrismaClient } from './generated/prisma/index'; // Corrected path
import 'dotenv/config'; // Use dotenv/config for loading .env

const prisma = new PrismaClient();

export const auth = Auth({
  adapter: PrismaAdapter(prisma),
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID as string,
      clientSecret: process.env.GITHUB_CLIENT_SECRET as string,
    }),
  ],
  callbacks: {
    // Optional: Add custom callbacks if needed
    // jwt: ({ token, user }) => {
    //   if (user) {
    //     token.id = user.id;
    //   }
    //   return token;
    // },
    // session: ({ session, token }) => {
    //   if (token) {
    //     session.user.id = token.id as string;
    //   }
    //   return session;
    // },
  },
  session: {
    // Use JSON Web Tokens for session instead of database sessions.
    // This option is important for making the JWT available to the Python backend.
    strategy: 'jwt',
  },
  jwt: {
    // You can define your own secret for JWTs.
    // This secret must be shared with the Python backend for verification.
    secret: process.env.AUTH_SECRET as string,
  },
  secret: process.env.AUTH_SECRET as string, // Master secret for Auth.js
  pages: {
    signIn: '/api/auth/signin', // Custom sign-in page if needed
  },
});