from django_ai_assistant import AIAssistant, method_tool
import json
import os


def load_instructions():
    """Carrega as instruções do arquivo markdown."""
    current_dir = os.path.dirname(__file__)
    instruction_file = os.path.join(current_dir, 'instruction', 'prompt_analise_inovacao_ISO56002.md')
    with open(instruction_file, 'r', encoding='utf-8') as f:
        return f.read()


APP_NAME = 'starbase'


class Inova360AIAssistant(AIAssistant):
    id = "asst_zmjcEDRXCAbZ41VtBZTXAtDh"
    name = "starbase"
    model = "gpt-4o-mini"
    instructions = load_instructions()



    # @method_tool
    # def get_base_startups(self) -> str:
    #
    #       Fornece uma lista de json contendo as startups disponíveis para comparação.
    #     """
    #     print('get_base_startups')
    #     from core.models import Organization
    #     organizations = Organization.objects.all().prefetch_related('tags').all()
    #
    #     org_list = [
    #         {
    #             "id": org.id,
    #             "Nome": org.name,
    #             "tags": ', '.join(tag.name for tag in org.tags.all()),
    #             "Descrição": org.description
    #         }
    #         for org in organizations
    #     ]
    #
    #     return json.dumps({"startups":org_list})



