// nodejs_backend/src/auth.ts

import { Auth, type AuthConfig } from '@auth/core';
import Google from '@auth/core/providers/google';
import GitHub from '@auth/core/providers/github'; // Fixed: removed duplicate 'from'
import { PrismaAdapter } from '@auth/prisma-adapter';
import { PrismaClient } from './generated/prisma/client'; // Use the client file directly
import 'dotenv/config';

const prisma = new PrismaClient();

// Export the AuthConfig object
export const authConfig: AuthConfig = {
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
    strategy: 'jwt',
  },
  jwt: {
    // Removed: secret: process.env.AUTH_SECRET as string,
  },
  secret: process.env.AUTH_SECRET as string, // Master secret for Auth.js
  pages: {
    signIn: '/api/auth/signin',
  },
};