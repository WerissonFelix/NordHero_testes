import os
import json
from groq import Groq
from dotenv import load_dotenv
from DataBase.repositories.score_repository import ScoreRepository
from DataBase.repositories.notes_hit_repository import NotesHitRepository
from DataBase.repositories.user_repository import UserRepository

load_dotenv()

class FocusAnalyzerGroq:
    def __init__(self):
        self.score_repo = ScoreRepository()
        self.notes_hit_repo = NotesHitRepository()
        self.user_repo = UserRepository()
        
        api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def get_user_stats(self, user_id):
        """Recupera e calcula estatísticas de foco do usuário"""
        scores = self.score_repo.get_all_by_user_id(user_id)
        if not scores:
            return None

        total_perfect = total_good = total_bad = total_miss = 0
        total_accuracy = 0.0
        all_ranks = []
        sessions_data = []

        for score in scores:
            notes_hit = self.notes_hit_repo.get_by_id(score.notes_hit_id)
            if notes_hit:
                total_perfect += notes_hit.qtd_perfect
                total_good += notes_hit.qtd_good
                total_bad += notes_hit.qtd_bad
                total_miss += notes_hit.qtd_miss
            total_accuracy += score.accuracy
            all_ranks.append(score.rank)
            sessions_data.append({
                "score": score.score,
                "accuracy": score.accuracy,
                "rank": score.rank
            })

        num_sessions = len(scores)
        avg_accuracy = total_accuracy / num_sessions if num_sessions > 0 else 0

        total_notes = total_perfect + total_good + total_bad + total_miss
        if total_notes > 0:
            perfect_pct = (total_perfect / total_notes) * 100
            good_pct = (total_good / total_notes) * 100
            bad_pct = (total_bad / total_notes) * 100
            miss_pct = (total_miss / total_notes) * 100
        else:
            perfect_pct = good_pct = bad_pct = miss_pct = 0

        if num_sessions > 1:
            import math
            mean_acc = avg_accuracy
            variance = sum((s["accuracy"] - mean_acc) ** 2 for s in sessions_data) / num_sessions
            consistency = 100 - (math.sqrt(variance) * 100)
            consistency = max(0, min(100, consistency))
        else:
            consistency = 100.0

        return {
            "avg_accuracy": avg_accuracy,
            "perfect_pct": perfect_pct,
            "good_pct": good_pct,
            "bad_pct": bad_pct,
            "miss_pct": miss_pct,
            "consistency": consistency,
            "total_sessions": num_sessions,
            "best_rank": max(set(all_ranks), key=all_ranks.count) if all_ranks else "N/A"
        }

    def build_analysis_prompt(self, stats: dict) -> str:
        prompt =f"""
            Você é um treinador de ritmo e foco especializado em jogos musicais.

            Com base nos dados abaixo de um jogador, responda SOMENTE com um JSON válido, sem texto extra, sem markdown, sem explicações fora do JSON. O formato deve ser exatamente:

            {{
            "focus_score": <número inteiro de 0 a 100 representando o nível de foco geral do jogador>,
            "analysis": "<um parágrafo encorajador em português brasileiro com: nível de foco, estilo de jogo ideal e duas dicas práticas>"
            }}

            Critérios para calcular o focus_score:
            - Accuracy alta e consistente → score mais alto
            - Alto percentual de Perfect → bônus significativo
            - Alto percentual de Miss → penalidade
            - Consistência entre partidas → peso importante
            - Ranking frequente também influencia

            Dados do jogador:
            - Média de accuracy: {stats['avg_accuracy']:.1f}%
            - Perfect: {stats['perfect_pct']:.1f}% | Good: {stats['good_pct']:.1f}% | Bad: {stats['bad_pct']:.1f}% | Miss: {stats['miss_pct']:.1f}%
            - Consistência entre partidas: {stats['consistency']:.1f}%
            - Total de partidas: {stats['total_sessions']}
            - Ranking mais frequente: {stats['best_rank']}
            """
        return prompt

    def analyze_user_focus(self, user_id: int):
        """
        Retorna um dicionário com:
          - focus_score (int, 0-100)
          - analysis (str)
          - error (str | None)
        """
        
        user = self.user_repo.get_by_id(user_id)
        user_name = user.name if user else f"Jogador {user_id}"

        stats = self.get_user_stats(user_id)
        if not stats:
            return f"{user_name}, você ainda não possui scores registrados. Jogue algumas partidas primeiro!"

        prompt = self.build_analysis_prompt(stats)

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Você é um analista experiente de performance em jogos musicais. "
                            "Responda SEMPRE e SOMENTE com JSON válido, sem nenhum texto fora do JSON."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=500,
            )

            raw = chat_completion.choices[0].message.content.strip()
            
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
                raw = raw.strip()

            data = json.loads(raw)

            focus_score = int(data.get("focus_score", 0))
            focus_score = max(0, min(100, focus_score))  # garante intervalo [0, 100]
            analysis = data.get("analysis", "")

            return {
                "focus_score": focus_score,
                "analysis": f"**Análise de foco para {user_name}** 🎯\n\n{analysis}",
                "error": None,
            }
            
        except json.JSONDecodeError as e:
            return {
                "focus_score": None,
                "analysis": f"O modelo retornou uma resposta inválida (não era JSON). Resposta bruta: {raw[:200]}",
                "error": f"json_decode_error: {e}",
            }
            
        except Exception as e:
            return {
                "focus_score": None,
                "analysis": f"Erro ao consultar o Groq: {type(e).__name__} - {e}",
                "error": str(e),
            }
