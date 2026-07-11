sed -i 's/from src.config.dependencies import get_current_user/from src.core.security import get_current_user/' src/dashboard/router.py

echo "Dashboard auth fixed"
