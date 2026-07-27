from telegram import Update
from telegram.ext import ContextTypes


async def users_list_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "👥 User List\n\n"
        "Database User Loading Ready ✅"
    )


async def rbac_roles_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "🔐 RBAC Roles\n\n"
        "OWNER\n"
        "ADMIN\n"
        "MEMBER"
    )


async def permissions_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    await query.message.reply_text(
        "🔑 Permissions Center\n\n"
        "User Permission Engine Ready ✅"
    )
