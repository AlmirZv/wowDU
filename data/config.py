from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("SUPERADMIN_ID")  # Тут у нас будет список из админов
ip = env.str("ip")  # Тоже str, но для айпи адреса хоста
SUPERADMIN_ID = env.int("SUPERADMIN_ID")

# PAYMENTS TOKENS
TESTPAY_TOKEN = env.str("TESTPAY_TOKEN")
SUPERADMIN_TOKEN = env.str("TESTPAY_TOKEN")

# PostgreSQL DATA
DB_USER = env.str("DB_USER")
DB_PASS = env.str("DB_PASS")
DB_NAME = env.str("DB_NAME")
DB_HOST = env.str("DB_HOST")


PGUSER = env.str("PGUSER")
PGPASSWORD = env.str("PGPASSWORD")
DATABASE = env.str("DATABASE")

POSTGRESURI = f"postgresql://{PGUSER}:{PGPASSWORD}@{ip}/{DATABASE}"

# shopAdmins
PIZZA_ADMINS = env.list("PIZZA_ADMINS")
