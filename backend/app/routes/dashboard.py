from fastapi import APIRouter

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# =========================
# Dashboard (placeholder)
# =========================
@router.get("/health")
def dashboard_health():
    return {
        "status": "ok",
        "message": "Dashboard ativo (vazio por enquanto)"
    }
