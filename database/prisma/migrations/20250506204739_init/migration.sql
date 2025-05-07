-- CreateEnum
CREATE TYPE "RoleEnum" AS ENUM ('user', 'admin');

-- CreateEnum
CREATE TYPE "StatusEnum" AS ENUM ('resolved', 'inProgress', 'pending');

-- CreateTable
CREATE TABLE "user" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "phoneNumber" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    "role" "RoleEnum" NOT NULL DEFAULT 'user',
    "refreshToken" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "user_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "complaint" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "trainNumber" TEXT NOT NULL,
    "pnrNumber" TEXT NOT NULL,
    "coachNumber" TEXT NOT NULL,
    "seatNumber" TEXT NOT NULL,
    "sourceStation" TEXT NOT NULL,
    "destinationStation" TEXT NOT NULL,
    "complaint" TEXT NOT NULL,
    "classification" TEXT,
    "sentiment" TEXT,
    "sentimentScore" DOUBLE PRECISION,
    "status" "StatusEnum" NOT NULL DEFAULT 'pending',
    "resolution" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "complaint_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "user_email_key" ON "user"("email");

-- CreateIndex
CREATE UNIQUE INDEX "user_phoneNumber_key" ON "user"("phoneNumber");

-- AddForeignKey
ALTER TABLE "complaint" ADD CONSTRAINT "complaint_userId_fkey" FOREIGN KEY ("userId") REFERENCES "user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
