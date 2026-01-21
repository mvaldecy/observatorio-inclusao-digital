import streamlit as st
import pandas as pd
import sys
import os

# Adiciona a raiz do projeto e o diretório streamlit ao sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
streamlit_path = os.path.join(root_path, 'streamlit')
for p in [root_path, streamlit_path]:
    if p not in sys.path:
        sys.path.append(p)

from utils.data_loader import get_analisador_individuos
from cetic.individuos.metadados_individuos import MetadadosIndividuos

st.set_page_config(page_title="Cetic Indivíduos", layout="wide")

st.title("📊 CETIC - TIC Indivíduos")

# Categorias de indicadores - TODOS os indicadores disponíveis
CATEGORIAS = {
    "🌐 Acesso e Uso Básico": {
        'C1': 'Já usou a Internet?',
        'C3': 'Última vez que usou Internet',
        'C3J3': 'Usuário de internet (ampliado)',
        'C4': 'Frequência de uso da Internet',
        'C1_COB_A': 'Já enviou/recebeu e-mails?',
        'C1_COB_B': 'Já mandou mensagens por WhatsApp/Telegram?',
        'C1_COB_C1': 'Já usou redes sociais (Facebook/TikTok)?',
        'C1_COB_D': 'Já buscou informações (Google/Bing)?',
    },
    "🚫 Barreiras de Acesso": {
        'C2_D': 'Não tem onde acessar',
        'C2_E': 'Muito caro',
        'C2_F': 'Preocupações com segurança/privacidade',
        'C2_G': 'Evitar conteúdo perigoso',
        'C2_I': 'Falta de interesse/necessidade',
        'C2_J': 'Não sabe usar',
        'C2_OUTRO': 'Outro motivo',
        'C2A': 'Principal motivo para não usar',
    },
    "💻 Dispositivos Utilizados": {
        'C5_A': 'Computador de mesa',
        'C5_B': 'Notebook',
        'C5_C': 'Tablet',
        'C5_D': 'Telefone celular',
        'C5_E': 'Videogame',
        'C5_F': 'Televisão',
        'C5_OUTRO': 'Outro aparelho',
        'C5_DISPOSITIVOS': 'Celular e computador (exclusivo/simultâneo)',
        'DISPOSITIVOS_TODOS': ['C5_A', 'C5_B', 'C5_C', 'C5_D', 'C5_E', 'C5_F'],
    },
    "📍 Locais de Acesso": {
        'C6_A': 'Em casa',
        'C6_B': 'No trabalho',
        'C6_C': 'Na escola/ensino',
        'C6_D': 'Casa de outra pessoa',
        'C6_E': 'Centro público gratuito',
        'C6_F': 'Centro público pago (lanhouse)',
        'C6_G': 'Deslocando-se (rua/ônibus/metrô)',
        'C6A': 'Local mais frequente',
        'LOCAIS_TODOS': ['C6_A', 'C6_B', 'C6_C', 'C6_D', 'C6_E', 'C6_F', 'C6_G'],
    },
    "💬 Comunicação": {
        'C7_A': 'E-mail',
        'C7_B': 'Mensagens instantâneas (WhatsApp/Skype)',
        'C7_C': 'Voz/vídeo (Skype/WhatsApp)',
        'C7_D1': 'Redes sociais (Facebook/Instagram/TikTok)',
        'C7_E': 'Listas de discussão/fóruns',
        'C7_F': 'Microblog (X/Twitter)',
    },
    "🔍 Busca de Informações": {
        'C8_A': 'Produtos e serviços',
        'C8_B': 'Saúde',
        'C8_C': 'Viagens e acomodações',
        'C8_D': 'Emprego/enviar currículos',
        'C8_E': 'Wikipédia',
        'C8_F': 'Sites de governo',
        'C8_G': 'Serviços públicos online',
        'C8_H': 'Transações financeiras',
        'C8_I': 'Pagamento/transferência Pix',
    },
    "🎬 Entretenimento": {
        'C9_A': 'Jogos online',
        'C9_B': 'Ouvir música (Spotify/Deezer/YouTube)',
        'C9_C': 'Vídeos/filmes/séries (YouTube/Netflix)',
        'C9_D': 'Jornais/revistas/notícias',
        'C9_E': 'Transmissões ao vivo/lives',
        'C9_F': 'Exposições e museus',
        'C9_G': 'Podcasts',
    },
    "📚 Educação e Trabalho": {
        'C10_A': 'Atividades/pesquisas escolares',
        'C10_B': 'Cursos à distância',
        'C10_C': 'Informações sobre cursos superiores',
        'C10_D': 'Estudar por conta própria',
        'C10_E': 'Armazenamento na nuvem (Dropbox/Drive)',
        'C10_F': 'Atividades de trabalho',
    },
    "🎨 Criação de Conteúdo": {
        'C11_A': 'Compartilhar conteúdo (textos/imagens/vídeos)',
        'C11_B': 'Criar/atualizar blogs/websites',
        'C11_C': 'Postar conteúdo próprio',
        'TC10_A': 'Postou textos que criou',
        'TC10_B': 'Postou imagens/fotos que criou',
        'TC10_C': 'Postou vídeos que criou',
        'TC10_D': 'Postou músicas que criou',
    },
    "🤖 Inteligência Artificial": {
        'C13A': 'Usou IA (ChatGPT/Copilot/Gemini)',
        'C13B_A': 'IA para trabalho profissional',
        'C13B_B': 'IA para pesquisa escolar',
        'C13B_C': 'IA para uso pessoal',
        'C13C_A': 'Não usou: falta de interesse',
        'C13C_B': 'Não usou: não conhecia',
        'C13C_C': 'Não usou: falta de habilidade',
        'C13C_D': 'Não usou: preocupações segurança',
    },
    "🎰 Apostas Online": {
        'C14_A': 'Loteria federal (Mega Sena/Lotofácil)',
        'C14_B': 'Cassino online (jogo do tigrinho)',
        'C14_C': 'Apostas esportivas (Bet365/Betano)',
        'C14_D': 'Rifas digitais/sorteios',
    },
    "🏛️ Governo Eletrônico": {
        'G1_A': 'Documentos pessoais (RG/CPF)',
        'G1_B': 'Saúde pública',
        'G1_C': 'Educação pública (ENEM/PROUNI)',
        'G1_D': 'INSS/FGTS/previdência',
        'G1_E': 'Impostos (IR/IPVA/IPTU)',
        'G1_F': 'Polícia e segurança',
        'G1_G': 'Transporte público',
        'G1_H': 'Justiça (processos/defensoria)',
        'G5_A': 'Acessou Gov.br para si',
        'G5_B': 'Acessou Gov.br para outra pessoa',
    },
    "🛒 Comércio Eletrônico": {
        'H2': 'Comprou/encomendou produtos online (12 meses)',
    },
    "💡 Habilidades Digitais": {
        'I1A_A': 'Copiar/mover arquivos',
        'I1A_B': 'Copiar e colar conteúdo',
        'I1A_C': 'Anexar documentos/imagens',
        'I1A_D': 'Usar fórmulas em planilhas',
        'I1A_E': 'Conectar/instalar equipamentos',
        'I1A_F': 'Instalar programas/aplicativos',
        'I1A_G': 'Criar apresentações',
        'I1A_H': 'Transferir arquivos entre dispositivos',
        'I1A_I': 'Programar (criar app/programa)',
        'I1A_J': 'Medidas de segurança (senhas fortes)',
        'I1A_K': 'Configurações de privacidade',
        'I1A_L': 'Verificar veracidade de informações',
        'HABILIDADES_BASICAS': ['I1A_A', 'I1A_B', 'I1A_C', 'I1A_F'],
        'HABILIDADES_AVANCADAS': ['I1A_D', 'I1A_G', 'I1A_I'],
        'HABILIDADES_SEGURANCA': ['I1A_J', 'I1A_K', 'I1A_L'],
    },
    "📱 Telefone Celular - Uso": {
        'J1': 'Usou telefone celular (3 meses)',
        'J5': 'Possui telefone celular',
        'J6': 'Tipo: pré ou pós-pago',
        'J2_A': 'Chamadas telefônicas',
        'J2_B': 'SMS',
        'J2_H1': 'E-mails',
        'J2_I1': 'Redes sociais',
        'J2_N': 'Mensagens pela Internet (WhatsApp)',
        'J2_L': 'Buscar informações (Google)',
    },
    "📱 Telefone Celular - Internet": {
        'J3': 'Usou Internet pelo celular',
        'J3A_A': 'Conexão 3G/4G/5G',
        'J3A_B': 'Conexão WiFi',
        'J7': 'Pacote de dados acabou',
        'J8A': 'O que fez quando pacote acabou',
        'J8B_C': 'Velocidade reduzida',
        'J8B_D': 'Comprou créditos/pacote adicional',
    },
    "🎵 Consumo Cultural - Música": {
        'TC2B_A': 'YouTube/Vimeo',
        'TC2B_B': 'Spotify/Deezer (assinatura)',
        'TC2B_C': 'iTunes (compra)',
        'TC2B_E': 'Rádio online',
        'TC3_A': 'Músicas estrangeiras',
        'TC3_B': 'Músicas brasileiras',
    },
    "🎬 Consumo Cultural - Vídeos": {
        'TC4_A': 'Filmes',
        'TC4_B': 'Séries',
        'TC4_C': 'Programas de TV',
        'TC4B_A': 'Vídeos de notícias',
        'TC4B_H': 'Tutoriais/videoaulas',
        'TC4B_I': 'Influenciadores/youtubers',
        'TC4C_A': 'YouTube/Vimeo',
        'TC4C_D1': 'Netflix/Disney+/streaming',
        'TC7_A': 'Filmes estrangeiros',
        'TC7_B': 'Filmes brasileiros',
    },
    "👥 Perfil Demográfico": {
        'SEXO': 'Sexo',
        'IDADE': 'Idade',
        'FAIXA_ETARIA': 'Faixa etária',
        'RACA': 'Cor/raça',
        'ESTUD': 'Frequenta escola/universidade',
        'GRAU_INST_1': 'Grau de instrução',
        'RENDA_PESSOAL': 'Renda pessoal',
        'RENDA_FAMILIAR_2': 'Renda familiar',
        'CLASSE_2015': 'Classe social',
        'PEA': 'Condição de atividade',
        'COD_UF': 'UF',
        'COD_REGIAO_2': 'Região',
    },
}

# Contar indicadores
total_indicadores = sum(1 for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, str))
total_comparativos = sum(1 for cat in CATEGORIAS.values() for k, v in cat.items() if isinstance(v, list))

st.markdown(f"""
### Selecione um Indicador para Análise
Escolha a categoria e depois o indicador específico que deseja analisar.

**Disponíveis:** {total_indicadores} indicadores individuais + {total_comparativos} análises comparativas
""")

# Seleção por categoria primeiro
col_cat, col_ind = st.columns([1, 2])

with col_cat:
    selected_category = st.selectbox(
        "📁 Categoria",
        options=list(CATEGORIAS.keys()),
        help="Selecione uma categoria de indicadores"
    )

# Planificar INDICADORES da categoria selecionada
INDICADORES_CATEGORIA = {}
for k, v in CATEGORIAS[selected_category].items():
    if isinstance(v, str):
        INDICADORES_CATEGORIA[k] = v
    else:
        INDICADORES_CATEGORIA[k] = f"COMPARATIVO: {k}"

with col_ind:
    selected_indicador_key = st.selectbox(
        "📊 Indicador",
        options=list(INDICADORES_CATEGORIA.keys()),
        format_func=lambda x: INDICADORES_CATEGORIA[x],
        help="Selecione o indicador específico"
    )

# Determinar se é análise múltipla
is_multiple = False
actual_indicador = selected_indicador_key

# Verificar se o indicador selecionado é uma lista (comparativo)
for cat in CATEGORIAS.values():
    if selected_indicador_key in cat and isinstance(cat[selected_indicador_key], list):
        is_multiple = True
        actual_indicador = cat[selected_indicador_key]
        break

# Obter label amigável
if is_multiple:
    label_indicador = f"📊 Comparativo: {selected_indicador_key}"
else:
    meta_col = getattr(MetadadosIndividuos, actual_indicador, None)
    label_indicador = getattr(meta_col, '_label', INDICADORES_CATEGORIA.get(actual_indicador, actual_indicador))

st.subheader(label_indicador)

# Carrega o analisador
analisador = get_analisador_individuos()

# Sidebar - Filtros
st.sidebar.header("Filtros")

def limpar_filtros():
    st.session_state['uf_ind'] = "Brasil"
    st.session_state['classe_ind'] = "Todas"
    st.session_state['renda_ind'] = "Todas"
    st.session_state['sexo_ind'] = "Todos"
    st.session_state['regiao_ind'] = "Brasil"
    st.session_state['faixa_etaria_ind'] = "Todas"

# Filtro de UF
ufs = MetadadosIndividuos.COD_UF._map
uf_options = ["Brasil"] + list(ufs.values())
selected_uf_label = st.sidebar.selectbox("UF", uf_options, key='uf_ind')

# Filtro de Classe Social
classes = MetadadosIndividuos.CLASSE_2015._map
class_options = ["Todas"] + list(classes.values())
selected_class_label = st.sidebar.selectbox("Classe Social", class_options, key='classe_ind')

# Filtro de Renda Familiar
rendas = MetadadosIndividuos.RENDA_FAMILIAR_2._map
renda_options = ["Todas"] + list(rendas.values())
selected_renda_label = st.sidebar.selectbox("Renda Familiar", renda_options, key='renda_ind')

# Filtro de Sexo
sexos = MetadadosIndividuos.SEXO._map
sexo_options = ["Todos"] + list(sexos.values())
selected_sexo_label = st.sidebar.selectbox("Sexo", sexo_options, key='sexo_ind')

# Filtro de Região
regioes = MetadadosIndividuos.COD_REGIAO_2._map
regiao_options = ["Brasil"] + list(regioes.values())
selected_regiao_label = st.sidebar.selectbox("Região", regiao_options, key='regiao_ind')

# Filtro de Faixa Etária
faixas_etarias = MetadadosIndividuos.FAIXA_ETARIA._map
faixa_options = ["Todas"] + list(faixas_etarias.values())
selected_faixa_label = st.sidebar.selectbox("Faixa Etária", faixa_options, key='faixa_etaria_ind')

st.sidebar.button("Limpar filtros", on_click=limpar_filtros)

# Preparar filtros para o analisador
filtros = []

def get_meta_value(meta_class, label_map, selected_label):
    if selected_label == "Todas" or selected_label == "Brasil" or selected_label == "Todos":
        return None
    val = [k for k, v in label_map.items() if v == selected_label][0]
    for attr in dir(meta_class):
        meta_val = getattr(meta_class, attr)
        if isinstance(meta_val, float) and meta_val == val:
            return meta_val
    return None

f_uf = get_meta_value(MetadadosIndividuos.COD_UF, ufs, selected_uf_label)
if f_uf: filtros.append(f_uf)

f_class = get_meta_value(MetadadosIndividuos.CLASSE_2015, classes, selected_class_label)
if f_class: filtros.append(f_class)

f_renda = get_meta_value(MetadadosIndividuos.RENDA_FAMILIAR_2, rendas, selected_renda_label)
if f_renda: filtros.append(f_renda)

f_sexo = get_meta_value(MetadadosIndividuos.SEXO, sexos, selected_sexo_label)
if f_sexo: filtros.append(f_sexo)

f_regiao = get_meta_value(MetadadosIndividuos.COD_REGIAO_2, regioes, selected_regiao_label)
if f_regiao: filtros.append(f_regiao)

f_faixa = get_meta_value(MetadadosIndividuos.FAIXA_ETARIA, faixas_etarias, selected_faixa_label)
if f_faixa: filtros.append(f_faixa)

# Executar análise
# Criamos uma cópia do dataframe para não afetar o original no analisador (que é cacheado)
df_filtrado = analisador.df.copy()

# Aplicar os filtros
for f in filtros:
    col = f.column
    df_filtrado = df_filtrado[df_filtrado[col] == f]

st.info(f"Registros encontrados: {len(df_filtrado):,}")

# Análise do Indicador Selecionado
if len(df_filtrado) > 0:
    res = analisador.analisar_indicador(actual_indicador, df_contexto=df_filtrado)
    
    if res is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.write("### Tabela de Resultados")
            st.dataframe(res, use_container_width=True)
            
        with col2:
            st.write("### Visualização")
            chart_data = res.copy()
            chart_data['Percentual_Num'] = chart_data['Percentual'].str.replace('%', '').astype(float)
            
            # Gráfico de barras
            st.bar_chart(chart_data, x="Descrição", y="Percentual_Num")
            
            # KPI (Apenas se tiver 'Sim')
            if not is_multiple:
                sim_row = res[res['Descrição'] == 'Sim']
                if not sim_row.empty:
                    st.metric(f"{selected_indicador_key} (Sim)", sim_row['Percentual'].values[0])
            else:
                top_row = chart_data.sort_values('Percentual_Num', ascending=False).iloc[0]
                st.metric(f"Maior: {top_row['Indicador']}", top_row['Percentual'])
else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.markdown("---")
st.caption("Fonte: Microdados da TIC Domicílios 2025 (CETIC.br)")
