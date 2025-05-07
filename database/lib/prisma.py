from prisma import Prisma

# Create a global instance placeholder
_prisma = None

def get_prisma_client() -> Prisma:
    global _prisma
    if _prisma is None:
        _prisma = Prisma()
        _prisma.connect()
    return _prisma