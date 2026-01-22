# app/services/notifications/alert_dispatcher.py
from app.services.alert_engine_service import AlertEngineService
from app.services.category_goal_alert_service import CategoryGoalAlertService
from app.services.notifications.email_service import EmailService
from sqlalchemy.orm import Session
from app.models.alert_history import AlertHistory

class AlertDispatcher:

    @staticmethod
    def send_alerts(db: Session, users: list, auto_whatsapp: bool = False):
        """
        Envia alertas financeiros para os usuários por e-mail.
        WhatsApp temporariamente desativado.
        """
        # 1️⃣ Gerar alertas
        alerts_data = AlertEngineService.generate(db)
        goals_alerts = CategoryGoalAlertService.analyze(db)
        alerts_data['alerts'].extend(goals_alerts)

        if not alerts_data['alerts']:
            print("✅ Nenhum alerta a enviar.")
            return

        # 2️⃣ Preparar mensagem resumida
        summary = alerts_data.get('summary', 'Alertas financeiros')
        messages = [f"[{a['level'].upper()}] {a['title']}: {a['message']}" for a in alerts_data['alerts']]
        full_message = f"{summary}\n\n" + "\n".join(messages)

        # 3️⃣ Enviar para cada usuário (apenas e-mail)
        for user in users:
            if 'email' in user:
                try:
                    EmailService.send_email(user['email'], "Alerta Financeiro", full_message)
                    print(f"✅ E-mail enviado: {summary}")
                except Exception as e:
                    print(f"❌ Falha ao enviar e-mail para {user['email']}: {e}")

            # 4️⃣ Registrar alertas no banco
            for alert in alerts_data['alerts']:
                try:
                    hist = AlertHistory(
                        title=alert['title'],
                        level=alert['level'],
                        message=alert['message']
                    )
                    db.add(hist)
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"❌ Falha ao registrar/enviar alerta para {user.get('email','?')}: {e}")

        print("📣 Todos os alertas processados com sucesso (WhatsApp desativado temporariamente).")
