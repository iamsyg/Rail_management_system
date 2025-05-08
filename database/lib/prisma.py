from prisma import Prisma

prisma = Prisma()

async def get_prisma_client() -> Prisma:
    global prisma
    if not prisma.is_connected():
        await prisma.connect()
    return prisma