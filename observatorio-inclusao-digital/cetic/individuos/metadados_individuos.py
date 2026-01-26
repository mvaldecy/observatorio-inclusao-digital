# -*- coding: utf-8 -*-
"""
METADADOS DE INDIVÍDUOS GERADOS AUTOMATICAMENTE
"""

class MetaValue(float):
    def __new__(cls, value, column):
        res = super(MetaValue, cls).__new__(cls, value)
        res.column = column
        return res

class MetadadosIndividuos:
    class QUEST:
        """Número de identificação do questionário"""
        _label = 'Número de identificação do questionário'
        pass

    class ID_DOMICILIO:
        """Número de identificação do domicílio"""
        _label = 'Número de identificação do domicílio'
        pass

    class ID_MORADOR:
        """Número de identificação do morador que foi selecionado para responder a pesquisa (id_morador do quadro domiciliar)"""
        _label = 'Número de identificação do morador que foi selecionado para responder a pesquisa (id_morador do quadro domiciliar)'
        MORADOR_1 = MetaValue(1.0, 'ID_MORADOR')
        MORADOR_2 = MetaValue(2.0, 'ID_MORADOR')
        MORADOR_3 = MetaValue(3.0, 'ID_MORADOR')
        MORADOR_4 = MetaValue(4.0, 'ID_MORADOR')
        MORADOR_5 = MetaValue(5.0, 'ID_MORADOR')
        MORADOR_6 = MetaValue(6.0, 'ID_MORADOR')
        MORADOR_7 = MetaValue(7.0, 'ID_MORADOR')
        MORADOR_8 = MetaValue(8.0, 'ID_MORADOR')
        MORADOR_9 = MetaValue(9.0, 'ID_MORADOR')
        MORADOR_10 = MetaValue(10.0, 'ID_MORADOR')
        MORADOR_11 = MetaValue(11.0, 'ID_MORADOR')
        MORADOR_12 = MetaValue(12.0, 'ID_MORADOR')
        MORADOR_13 = MetaValue(13.0, 'ID_MORADOR')
        MORADOR_14 = MetaValue(14.0, 'ID_MORADOR')
        MORADOR_15 = MetaValue(15.0, 'ID_MORADOR')
        MORADOR_16 = MetaValue(16.0, 'ID_MORADOR')
        MORADOR_17 = MetaValue(17.0, 'ID_MORADOR')
        MORADOR_18 = MetaValue(18.0, 'ID_MORADOR')
        MORADOR_19 = MetaValue(19.0, 'ID_MORADOR')
        MORADOR_20 = MetaValue(20.0, 'ID_MORADOR')
        NENHUM = MetaValue(98.0, 'ID_MORADOR')
        _map = {1.0: 'Morador 1', 2.0: 'Morador 2', 3.0: 'Morador 3', 4.0: 'Morador 4', 5.0: 'Morador 5', 6.0: 'Morador 6', 7.0: 'Morador 7', 8.0: 'Morador 8', 9.0: 'Morador 9', 10.0: 'Morador 10', 11.0: 'Morador 11', 12.0: 'Morador 12', 13.0: 'Morador 13', 14.0: 'Morador 14', 15.0: 'Morador 15', 16.0: 'Morador 16', 17.0: 'Morador 17', 18.0: 'Morador 18', 19.0: 'Morador 19', 20.0: 'Morador 20', 98.0: 'Nenhum'}

    class SEXO:
        """Sexo"""
        _label = 'Sexo'
        MASCULINO = MetaValue(1.0, 'SEXO')
        FEMININO = MetaValue(2.0, 'SEXO')
        _map = {1.0: 'Masculino', 2.0: 'Feminino'}

    class IDADE:
        """Idade do respondente"""
        _label = 'Idade do respondente'
        pass

    class FAIXA_ETARIA:
        """Faixa etária"""
        _label = 'Faixa etária'
        DE_10_A_15_ANOS = MetaValue(1.0, 'FAIXA_ETARIA')
        DE_16_A_24_ANOS = MetaValue(2.0, 'FAIXA_ETARIA')
        DE_25_A_34_ANOS = MetaValue(3.0, 'FAIXA_ETARIA')
        DE_35_A_44_ANOS = MetaValue(4.0, 'FAIXA_ETARIA')
        DE_45_A_59_ANOS = MetaValue(5.0, 'FAIXA_ETARIA')
        V_60_ANOS_OU_MAIS = MetaValue(6.0, 'FAIXA_ETARIA')
        _map = {1.0: 'De 10 a 15 anos', 2.0: 'De 16 a 24 anos', 3.0: 'De 25 a 34 anos', 4.0: 'De 35 a 44 anos', 5.0: 'De 45 a 59 anos', 6.0: '60 anos ou mais'}

    class GRAU_INSTRUCAO_1:
        """Grau de instrução informado pelo respondente"""
        _label = 'Grau de instrução informado pelo respondente'
        NAO_FREQUENTOU_ESCOLA = MetaValue(1.0, 'GRAU_INSTRUCAO_1')
        ATE_CRECHE_OU_PRE_ESCOLA_INCOMPLETO = MetaValue(2.0, 'GRAU_INSTRUCAO_1')
        ATE_CRECHE_OU_PRE_ESCOLA_COMPLETO = MetaValue(3.0, 'GRAU_INSTRUCAO_1')
        CLASSE_DE_ALFABETIZACAO___CA = MetaValue(4.0, 'GRAU_INSTRUCAO_1')
        ALFABETIZACAO_DE_JOVENS_E_ADULTOS = MetaValue(5.0, 'GRAU_INSTRUCAO_1')
        PRIMEIROS_ANOS_CICLOS_DA_EJA_DO_ENSINO_FUNDAMENTAL_OU_SUPLETIVO_DO_1O_GRAU = MetaValue(6.0, 'GRAU_INSTRUCAO_1')
        ULTIMO_ANO_CICLO_DA_EJA_DO_ENSINO_FUNDAMENTAL_OU_SUPLETIVO_DO_1O_GRAU = MetaValue(7.0, 'GRAU_INSTRUCAO_1')
        PRIMEIROS_ANOS_CICLOS_DA_EJA_DO_ENSINO_MEDIO_OU_SUPLETIVO_DO_2O_GRAU = MetaValue(8.0, 'GRAU_INSTRUCAO_1')
        ULTIMO_ANO_CICLO_DA_EJA_DO_ENSINO_MEDIO_OU_SUPLETIVO_DO_2O_GRAU = MetaValue(9.0, 'GRAU_INSTRUCAO_1')
        V_1O_A_4O_ANO_DO_ENSINO_FUNDAMENTAL_I_1A_A_3A_SERIE_DO_PRIMARIO_1O_GRAU = MetaValue(10.0, 'GRAU_INSTRUCAO_1')
        V_5O_ANO_DO_ENSINO_FUNDAMENTAL_I_4A_SERIE_DO_PRIMARIO_1O_GRAU = MetaValue(11.0, 'GRAU_INSTRUCAO_1')
        V_6O_A_8O_ANO_DO_FUNDAMENTAL_II_5A_A_7A_SERIE_DO_GINASIO_1O_GRAU = MetaValue(12.0, 'GRAU_INSTRUCAO_1')
        V_9O_ANO_DO_FUNDAMENTAL_II_8A_SERIE_DO_GINASIO_1O_GRAU = MetaValue(13.0, 'GRAU_INSTRUCAO_1')
        V_1O_E_2O_ANO_DO_ENSINO_MEDIO___1A_E_2A_SERIE_DO_COLEGIAL_2O_GRAU = MetaValue(14.0, 'GRAU_INSTRUCAO_1')
        V_3O_ANO_DO_ENSINO_MEDIO___3A_SERIE_DO_COLEGIAL_2O_GRAU = MetaValue(15.0, 'GRAU_INSTRUCAO_1')
        SUPERIOR_INCOMPLETO = MetaValue(16.0, 'GRAU_INSTRUCAO_1')
        SUPERIOR_COMPLETO = MetaValue(17.0, 'GRAU_INSTRUCAO_1')
        ESPECIALIZACAO_DE_NIVEL_SUPERIOR = MetaValue(18.0, 'GRAU_INSTRUCAO_1')
        MESTRADO = MetaValue(19.0, 'GRAU_INSTRUCAO_1')
        DOUTORADO = MetaValue(20.0, 'GRAU_INSTRUCAO_1')
        NAO_SABE = MetaValue(97.0, 'GRAU_INSTRUCAO_1')
        NAO_RESPONDEU = MetaValue(98.0, 'GRAU_INSTRUCAO_1')
        _map = {1.0: 'Não frequentou escola', 2.0: 'Até creche ou pré-escola incompleto', 3.0: 'Até creche ou pré-escola completo', 4.0: 'Classe de alfabetização - CA', 5.0: 'Alfabetização de jovens e adultos', 6.0: 'Primeiros anos/ciclos da EJA do Ensino Fundamental ou supletivo do 1º grau', 7.0: 'Último ano/ciclo da EJA do Ensino Fundamental ou supletivo do 1º grau', 8.0: 'Primeiros anos/ciclos da EJA do Ensino Médio ou supletivo do 2º grau', 9.0: 'Último ano/ciclo da EJA do Ensino Médio ou supletivo do 2º grau', 10.0: '1º a 4º ano do Ensino Fundamental I, 1ª a 3ª série do Primário/1º Grau', 11.0: '5º ano do Ensino Fundamental I, 4ª série do Primário/1º Grau', 12.0: '6º a 8º ano do Fundamental II, 5ª a 7ª série do Ginásio/1º grau', 13.0: '9º ano do Fundamental II, 8ª série do Ginásio/1º Grau', 14.0: '1º e 2º ano do Ensino Médio - 1ª e 2ª série do Colegial/2º grau', 15.0: '3º ano do Ensino Médio - 3ª série do Colegial/2º grau', 16.0: 'Superior incompleto', 17.0: 'Superior completo', 18.0: 'Especialização de nível superior', 19.0: 'Mestrado', 20.0: 'Doutorado', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class ESTUD:
        """Atualmente você frequenta escola ou universidade? Mesmo que suas aulas estejam interrompidas agora, considere que sim."""
        _label = 'Atualmente você frequenta escola ou universidade? Mesmo que suas aulas estejam interrompidas agora, considere que sim.'
        NAO = MetaValue(0.0, 'ESTUD')
        SIM = MetaValue(1.0, 'ESTUD')
        NAO_SABE = MetaValue(97.0, 'ESTUD')
        NAO_RESPONDEU = MetaValue(98.0, 'ESTUD')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class APOSENT:
        """O(a) sr.(a) é aposentado(a) ou pensionista?"""
        _label = 'O(a) sr.(a) é aposentado(a) ou pensionista?'
        NAO = MetaValue(0.0, 'APOSENT')
        SIM = MetaValue(1.0, 'APOSENT')
        NAO_SABE = MetaValue(97.0, 'APOSENT')
        NAO_RESPONDEU = MetaValue(98.0, 'APOSENT')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class PEA:
        """Condição de atividade"""
        _label = 'Condição de atividade'
        TRABALHA_EM_ATIVIDADE_REMUNERADA_PEA = MetaValue(1.0, 'PEA')
        TRABALHA_EM_ATIVIDADE_NAO_REMUNERADA_COMO_AJUDANTE_PEA = MetaValue(2.0, 'PEA')
        TRABALHA_MAS_ESTA_AFASTADO_PEA = MetaValue(3.0, 'PEA')
        TOMOU_PROVIDENCIA_PARA_CONSEGUIR_TRABALHO_NOS_ULTIMOS_30_DIAS_PEA = MetaValue(4.0, 'PEA')
        NAO_TRABALHA_E_NAO_PROCUROU_TRABALHO_NOS_ULTIMOS_30_DIAS_NAO_PEA = MetaValue(5.0, 'PEA')
        _map = {1.0: 'Trabalha em atividade remunerada (PEA)', 2.0: 'Trabalha em atividade não remunerada, como ajudante (PEA)', 3.0: 'Trabalha mas está afastado (PEA)', 4.0: 'Tomou providência para conseguir trabalho nos últimos 30 dias (PEA)', 5.0: 'Não trabalha e não procurou trabalho nos últimos 30 dias (NÃO PEA)'}

    class OCUP_12:
        """Nesse trabalho, o(a) sr.(a) era:"""
        _label = 'Nesse trabalho, o(a) sr.(a) era:'
        TRABALHADOR_DOMESTICO = MetaValue(1.0, 'OCUP_12')
        MILITAR_DO_EXERCITO_DA_MARINHA_DA_AERONAUTICA_DA_POLICIA_MILITAR_OU_DO_CORPO_DE_BOMBEIROS_MILITAR = MetaValue(2.0, 'OCUP_12')
        EMPREGADO_DO_SETOR_PRIVADO = MetaValue(3.0, 'OCUP_12')
        EMPREGADO_DO_SETOR_PUBLICO_INCLUSIVE_EMPRESAS_DE_ECONOMIA_MISTA = MetaValue(4.0, 'OCUP_12')
        EMPREGADOR = MetaValue(5.0, 'OCUP_12')
        CONTA_PROPRIA = MetaValue(6.0, 'OCUP_12')
        TRABALHADOR_FAMILIAR_NAO_REMUNERADO = MetaValue(7.0, 'OCUP_12')
        NAO_SE_APLICA = MetaValue(99.0, 'OCUP_12')
        _map = {1.0: 'Trabalhador doméstico', 2.0: 'Militar do exército, da marinha, da aeronáutica, da polícia militar ou do corpo de bombeiros militar', 3.0: 'Empregado do setor privado', 4.0: 'Empregado do setor público (inclusive empresas de economia mista)', 5.0: 'Empregador', 6.0: 'Conta própria', 7.0: 'Trabalhador familiar não remunerado', 99.0: 'Não se aplica'}

    class OCUP_29:
        """Nesse trabalho, o(a) sr.(a) tinha carteira de trabalho assinada?"""
        _label = 'Nesse trabalho, o(a) sr.(a) tinha carteira de trabalho assinada?'
        NAO = MetaValue(0.0, 'OCUP_29')
        SIM = MetaValue(1.0, 'OCUP_29')
        NAO_SE_APLICA = MetaValue(99.0, 'OCUP_29')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class OCUP_32:
        """O(a) sr.(a) era contribuinte do INSS por esse trabalho?"""
        _label = 'O(a) sr.(a) era contribuinte do INSS por esse trabalho?'
        NAO = MetaValue(0.0, 'OCUP_32')
        SIM = MetaValue(1.0, 'OCUP_32')
        NAO_SE_APLICA = MetaValue(99.0, 'OCUP_32')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class RENDA_PESSOAL:
        """Renda pessoal"""
        _label = 'Renda pessoal'
        ATE_R_151800 = MetaValue(1.0, 'RENDA_PESSOAL')
        DE_R_151801_ATE_R_303600 = MetaValue(2.0, 'RENDA_PESSOAL')
        DE_R_303601_ATE_R_455400 = MetaValue(3.0, 'RENDA_PESSOAL')
        DE_R_455401_ATE_R_759000 = MetaValue(4.0, 'RENDA_PESSOAL')
        DE_R_759001_ATE_R_1518000 = MetaValue(5.0, 'RENDA_PESSOAL')
        DE_R_1518001_ATE_R_3036000 = MetaValue(6.0, 'RENDA_PESSOAL')
        DE_R_3036001_ATE_R_4554000 = MetaValue(7.0, 'RENDA_PESSOAL')
        MAIS_DE_R_4554000 = MetaValue(8.0, 'RENDA_PESSOAL')
        NAO_TEM_RENDA = MetaValue(9.0, 'RENDA_PESSOAL')
        NAO_SABE = MetaValue(97.0, 'RENDA_PESSOAL')
        NAO_RESPONDEU = MetaValue(98.0, 'RENDA_PESSOAL')
        _map = {1.0: 'Até R$ 1.518,00', 2.0: 'De R$ 1.518,01 até R$ 3.036,00', 3.0: 'De R$ 3.036,01 até R$ 4.554,00', 4.0: 'De R$ 4.554,01 até R$ 7.590,00', 5.0: 'De R$ 7.590,01 até R$ 15.180,00', 6.0: 'De R$ 15.180,01 até R$ 30.360,00', 7.0: 'De R$ 30.360,01 até R$ 45.540,00', 8.0: 'Mais de R$ 45.540,00', 9.0: 'Não tem renda', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class RELIGIAO:
        """Religião ou culto"""
        _label = 'Religião ou culto'
        CATOLICA = MetaValue(1.0, 'RELIGIAO')
        LUTERANA__PRESBITERIANA__METODISTA__BATISTA = MetaValue(2.0, 'RELIGIAO')
        OUTRAS_IGREJAS_EVANGELICAS = MetaValue(3.0, 'RELIGIAO')
        OUTRAS_RELIGIOSIDADES_CRISTAS = MetaValue(4.0, 'RELIGIAO')
        ISLAMISMO__MUCULMANO = MetaValue(5.0, 'RELIGIAO')
        ESPIRITA = MetaValue(6.0, 'RELIGIAO')
        UMBANDA = MetaValue(7.0, 'RELIGIAO')
        CANDOMBLE = MetaValue(8.0, 'RELIGIAO')
        JUDAISMO = MetaValue(9.0, 'RELIGIAO')
        HINDUISMO = MetaValue(10.0, 'RELIGIAO')
        BUDISMO = MetaValue(11.0, 'RELIGIAO')
        SEM_RELIGIAO = MetaValue(12.0, 'RELIGIAO')
        AGNOSTICO = MetaValue(13.0, 'RELIGIAO')
        ATEU = MetaValue(14.0, 'RELIGIAO')
        OUTRAS_RELIGIOES = MetaValue(15.0, 'RELIGIAO')
        OUTRAS_RELIGIOES = MetaValue(16.0, 'RELIGIAO')
        NAO_RESPONDEU = MetaValue(98.0, 'RELIGIAO')
        _map = {1.0: 'Católica', 2.0: 'Luterana/ Presbiteriana/ Metodista/ Batista', 3.0: 'Outras Igrejas Evangélicas', 4.0: 'Outras religiosidades cristãs', 5.0: 'Islamismo/ Muçulmano', 6.0: 'Espírita', 7.0: 'Umbanda', 8.0: 'Candomblé', 9.0: 'Judaismo', 10.0: 'Hinduismo', 11.0: 'Budismo', 12.0: 'Sem religião', 13.0: 'Agnóstico', 14.0: 'Ateu', 15.0: 'Outras religiões', 16.0: 'Outras religiões', 98.0: 'Não respondeu'}

    class RACA:
        """Cor ou raça declarada pelo respondente"""
        _label = 'Cor ou raça declarada pelo respondente'
        BRANCA = MetaValue(1.0, 'RACA')
        PRETA = MetaValue(2.0, 'RACA')
        PARDA = MetaValue(3.0, 'RACA')
        AMARELA = MetaValue(4.0, 'RACA')
        INDIGENA = MetaValue(5.0, 'RACA')
        NAO_RESPONDEU = MetaValue(98.0, 'RACA')
        _map = {1.0: 'Branca', 2.0: 'Preta', 3.0: 'Parda', 4.0: 'Amarela', 5.0: 'Indígena', 98.0: 'Não respondeu'}

    class C1:
        """O respondente já usou a Internet?"""
        _label = 'O respondente já usou a Internet?'
        NAO = MetaValue(0.0, 'C1')
        SIM = MetaValue(1.0, 'C1')
        NAO_SABE = MetaValue(97.0, 'C1')
        NAO_RESPONDEU = MetaValue(98.0, 'C1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class C2_I:
        """O respondente nunca usou a Internet por falta de interesse ou necessidade?"""
        _label = 'O respondente nunca usou a Internet por falta de interesse ou necessidade?'
        NAO = MetaValue(0.0, 'C2_I')
        SIM = MetaValue(1.0, 'C2_I')
        NAO_SABE = MetaValue(97.0, 'C2_I')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_I')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_I')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_J:
        """O respondente nunca usou a Internet por não saber usar?"""
        _label = 'O respondente nunca usou a Internet por não saber usar?'
        NAO = MetaValue(0.0, 'C2_J')
        SIM = MetaValue(1.0, 'C2_J')
        NAO_SABE = MetaValue(97.0, 'C2_J')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_J')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_J')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_D:
        """O respondente nunca usou a Internet por não ter onde acessar?"""
        _label = 'O respondente nunca usou a Internet por não ter onde acessar?'
        NAO = MetaValue(0.0, 'C2_D')
        SIM = MetaValue(1.0, 'C2_D')
        NAO_SABE = MetaValue(97.0, 'C2_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_E:
        """O respondente nunca usou a Internet por ser muito caro?"""
        _label = 'O respondente nunca usou a Internet por ser muito caro?'
        NAO = MetaValue(0.0, 'C2_E')
        SIM = MetaValue(1.0, 'C2_E')
        NAO_SABE = MetaValue(97.0, 'C2_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_F:
        """O respondente nunca usou a Internet por preocupações com segurança ou privacidade?"""
        _label = 'O respondente nunca usou a Internet por preocupações com segurança ou privacidade?'
        NAO = MetaValue(0.0, 'C2_F')
        SIM = MetaValue(1.0, 'C2_F')
        NAO_SABE = MetaValue(97.0, 'C2_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_G:
        """O respondente nunca usou a Internet para evitar o contato com conteúdo perigoso?"""
        _label = 'O respondente nunca usou a Internet para evitar o contato com conteúdo perigoso?'
        NAO = MetaValue(0.0, 'C2_G')
        SIM = MetaValue(1.0, 'C2_G')
        NAO_SABE = MetaValue(97.0, 'C2_G')
        NAO_RESPONDEU = MetaValue(98.0, 'C2_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C2_OUTRO:
        """O respondente nunca usou a Internet por outro motivo?"""
        _label = 'O respondente nunca usou a Internet por outro motivo?'
        NAO = MetaValue(0.0, 'C2_OUTRO')
        SIM = MetaValue(1.0, 'C2_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C2_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C2A:
        """E qual desses motivos é o principal?"""
        _label = 'E qual desses motivos é o principal?'
        POR_NAO_TER_ONDE_ACESSAR = MetaValue(4.0, 'C2A')
        POR_SER_MUITO_CARO = MetaValue(5.0, 'C2A')
        POR_TER_PREOCUPACOES_COM_SEGURANCA_OU_PRIVACIDADE = MetaValue(6.0, 'C2A')
        PARA_EVITAR_O_CONTATO_COM_CONTEUDO_PERIGOSO = MetaValue(7.0, 'C2A')
        OUTROS = MetaValue(8.0, 'C2A')
        POR_FALTA_DE_NECESSIDADE = MetaValue(9.0, 'C2A')
        POR_NAO_SABER_USAR = MetaValue(10.0, 'C2A')
        NAO_SABE = MetaValue(97.0, 'C2A')
        NAO_RESPONDEU = MetaValue(98.0, 'C2A')
        NAO_SE_APLICA = MetaValue(99.0, 'C2A')
        _map = {4.0: 'Por não ter onde acessar', 5.0: 'Por ser muito caro', 6.0: 'Por ter preocupações com segurança ou privacidade', 7.0: 'Para evitar o contato com conteúdo perigoso', 8.0: 'Outros', 9.0: 'Por falta de necessidade', 10.0: 'Por não saber usar', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C3:
        """Quando o respondente usou a Internet pela última vez?"""
        _label = 'Quando o respondente usou a Internet pela última vez?'
        HA_MENOS_DE_3_MESES = MetaValue(1.0, 'C3')
        ENTRE_3_MESES_E_12_MESES = MetaValue(2.0, 'C3')
        MAIS_DE_12_MESES_ATRAS = MetaValue(3.0, 'C3')
        NAO_SE_APLICA = MetaValue(99.0, 'C3')
        _map = {1.0: 'Há menos de 3 meses', 2.0: 'Entre 3 meses e 12 meses', 3.0: 'Mais de 12 meses atrás', 99.0: 'Não se aplica'}

    class C4:
        """Em média, com que freqüência o respondente usou a Internet nos últimos 3 meses?"""
        _label = 'Em média, com que freqüência o respondente usou a Internet nos últimos 3 meses?'
        TODOS_OS_DIAS_OU_QUASE_TODOS_OS_DIAS = MetaValue(1.0, 'C4')
        PELO_MENOS_UMA_VEZ_POR_SEMANA = MetaValue(2.0, 'C4')
        PELO_MENOS_UMA_VEZ_POR_MES = MetaValue(3.0, 'C4')
        MENOS_DO_QUE_UMA_VEZ_POR_MES = MetaValue(4.0, 'C4')
        NAO_SE_APLICA = MetaValue(99.0, 'C4')
        _map = {1.0: 'Todos os dias ou quase todos os dias', 2.0: 'Pelo menos uma vez por semana', 3.0: 'Pelo menos uma vez por mês', 4.0: 'Menos do que uma vez por mês', 99.0: 'Não se aplica'}

    class C5_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet no computador de mesa?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet no computador de mesa?'
        NAO = MetaValue(0.0, 'C5_A')
        SIM = MetaValue(1.0, 'C5_A')
        NAO_SABE = MetaValue(97.0, 'C5_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet no notebook?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet no notebook?'
        NAO = MetaValue(0.0, 'C5_B')
        SIM = MetaValue(1.0, 'C5_B')
        NAO_SABE = MetaValue(97.0, 'C5_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet no Tablet?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet no Tablet?'
        NAO = MetaValue(0.0, 'C5_C')
        SIM = MetaValue(1.0, 'C5_C')
        NAO_SABE = MetaValue(97.0, 'C5_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_D:
        """Nos últimos 3 meses, o respondente utilizou a Internet no telefone celular?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet no telefone celular?'
        NAO = MetaValue(0.0, 'C5_D')
        SIM = MetaValue(1.0, 'C5_D')
        NAO_SABE = MetaValue(97.0, 'C5_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_E:
        """Nos últimos 3 meses, o respondente utilizou a Internet no videogame?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet no videogame?'
        NAO = MetaValue(0.0, 'C5_E')
        SIM = MetaValue(1.0, 'C5_E')
        NAO_SABE = MetaValue(97.0, 'C5_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_F:
        """Nos últimos 3 meses, o respondente utilizou a Internet na televisão?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet na televisão?'
        NAO = MetaValue(0.0, 'C5_F')
        SIM = MetaValue(1.0, 'C5_F')
        NAO_SABE = MetaValue(97.0, 'C5_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_OUTRO:
        """Nos últimos 3 meses, o respondente utilizou a Internet em outro aparelho?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet em outro aparelho?'
        NAO = MetaValue(0.0, 'C5_OUTRO')
        SIM = MetaValue(1.0, 'C5_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_A:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet em casa?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet em casa?'
        NAO = MetaValue(0.0, 'C6_A')
        SIM = MetaValue(1.0, 'C6_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_B:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet no trabalho?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet no trabalho?'
        NAO = MetaValue(0.0, 'C6_B')
        SIM = MetaValue(1.0, 'C6_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_C:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet na escola ou estabelecimento de ensino?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet na escola ou estabelecimento de ensino?'
        NAO = MetaValue(0.0, 'C6_C')
        SIM = MetaValue(1.0, 'C6_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_D:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?'
        NAO = MetaValue(0.0, 'C6_D')
        SIM = MetaValue(1.0, 'C6_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_E:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?'
        NAO = MetaValue(0.0, 'C6_E')
        SIM = MetaValue(1.0, 'C6_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_F:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou Internet café?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou Internet café?'
        NAO = MetaValue(0.0, 'C6_F')
        SIM = MetaValue(1.0, 'C6_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_G:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet enquanto se desloca, como por exemplo na rua, no ônibus, no metrô, no carro?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet enquanto se desloca, como por exemplo na rua, no ônibus, no metrô, no carro?'
        NAO = MetaValue(0.0, 'C6_G')
        SIM = MetaValue(1.0, 'C6_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_OUTRO:
        """Pensando nos últimos 3 meses, o respondente utilizou a Internet em outro lugar?"""
        _label = 'Pensando nos últimos 3 meses, o respondente utilizou a Internet em outro lugar?'
        NAO = MetaValue(0.0, 'C6_OUTRO')
        SIM = MetaValue(1.0, 'C6_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6A:
        """Em qual desses locais o respondente usou a Internet com mais freqüência?"""
        _label = 'Em qual desses locais o respondente usou a Internet com mais freqüência?'
        EM_CASA = MetaValue(1.0, 'C6A')
        NO_TRABALHO = MetaValue(2.0, 'C6A')
        NA_ESCOLA_OU_ESTABELECIMENTO_DE_ENSINO = MetaValue(3.0, 'C6A')
        NA_CASA_DE_OUTRA_PESSOA_COMO_POR_EXEMPLO_AMIGO_VIZINHO_OU_FAMILIAR = MetaValue(4.0, 'C6A')
        CENTRO_PUBLICO_DE_ACESSO_GRATUITO_COMO_POR_EXEMPLO_TELECENTRO_BIBLIOTECA_OU_ENTIDADE_COMUNITARIA = MetaValue(5.0, 'C6A')
        CENTRO_PUBLICO_DE_ACESSO_PAGO_COMO_POR_EXEMPLO_LANHOUSE_CYBER_CAFE_OU_INTERNET_CAFE = MetaValue(6.0, 'C6A')
        ENQUANTO_SE_DESLOCA_COMO_POR_EXEMPLO_NA_RUA_NO_ONIBUS_NO_METRO_OU_NO_CARRO = MetaValue(7.0, 'C6A')
        OUTRO_LUGAR = MetaValue(8.0, 'C6A')
        NAO_SABE = MetaValue(97.0, 'C6A')
        NAO_RESPONDEU = MetaValue(98.0, 'C6A')
        NAO_SE_APLICA = MetaValue(99.0, 'C6A')
        _map = {1.0: 'Em casa', 2.0: 'No trabalho', 3.0: 'Na escola ou estabelecimento de ensino', 4.0: 'Na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar', 5.0: 'Centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária', 6.0: 'Centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou Internet café', 7.0: 'Enquanto se desloca, como por exemplo na rua, no ônibus, no metrô ou no carro', 8.0: 'Outro lugar', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet para enviar e receber e-mail?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para enviar e receber e-mail?'
        NAO = MetaValue(0.0, 'C7_A')
        SIM = MetaValue(1.0, 'C7_A')
        NAO_SABE = MetaValue(97.0, 'C7_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet para enviar mensagens instantâneas (como, por exemplo,  por Facebook, Skype e Whatsapp)?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para enviar mensagens instantâneas (como, por exemplo,  por Facebook, Skype e Whatsapp)?'
        NAO = MetaValue(0.0, 'C7_B')
        SIM = MetaValue(1.0, 'C7_B')
        NAO_SABE = MetaValue(97.0, 'C7_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet para conversar por voz ou vídeo através de programas como Skype ou  Whatsapp?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para conversar por voz ou vídeo através de programas como Skype ou  Whatsapp?'
        NAO = MetaValue(0.0, 'C7_C')
        SIM = MetaValue(1.0, 'C7_C')
        NAO_SABE = MetaValue(97.0, 'C7_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_D1:
        """Nos últimos 3 meses, o respondente usou redes sociais, como Facebook, Instagram ou TikTok?"""
        _label = 'Nos últimos 3 meses, o respondente usou redes sociais, como Facebook, Instagram ou TikTok?'
        NAO = MetaValue(0.0, 'C7_D1')
        SIM = MetaValue(1.0, 'C7_D1')
        NAO_SABE = MetaValue(97.0, 'C7_D1')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_D1')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_D1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_E:
        """Nos últimos 3 meses,  o respondente utilizou a Internet para participar de listas de discussão ou fóruns?"""
        _label = 'Nos últimos 3 meses,  o respondente utilizou a Internet para participar de listas de discussão ou fóruns?'
        NAO = MetaValue(0.0, 'C7_E')
        SIM = MetaValue(1.0, 'C7_E')
        NAO_SABE = MetaValue(97.0, 'C7_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C7_F:
        """Nos últimos 3 meses,  o respondente utilizou a Internet para usar microblog como, por exemplo, o X,antigo Twitter?"""
        _label = 'Nos últimos 3 meses,  o respondente utilizou a Internet para usar microblog como, por exemplo, o X,antigo Twitter?'
        NAO = MetaValue(0.0, 'C7_F')
        SIM = MetaValue(1.0, 'C7_F')
        NAO_SABE = MetaValue(97.0, 'C7_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C7_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C7_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações sobre produtos e serviços?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações sobre produtos e serviços?'
        NAO = MetaValue(0.0, 'C8_A')
        SIM = MetaValue(1.0, 'C8_A')
        NAO_SABE = MetaValue(97.0, 'C8_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações relacionadas à saúde ou a serviços de saúde?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações relacionadas à saúde ou a serviços de saúde?'
        NAO = MetaValue(0.0, 'C8_B')
        SIM = MetaValue(1.0, 'C8_B')
        NAO_SABE = MetaValue(97.0, 'C8_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações sobre viagens e acomodações?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações sobre viagens e acomodações?'
        NAO = MetaValue(0.0, 'C8_C')
        SIM = MetaValue(1.0, 'C8_C')
        NAO_SABE = MetaValue(97.0, 'C8_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_D:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar emprego ou enviar currículos?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar emprego ou enviar currículos?'
        NAO = MetaValue(0.0, 'C8_D')
        SIM = MetaValue(1.0, 'C8_D')
        NAO_SABE = MetaValue(97.0, 'C8_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_E:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações em sites de enciclopédia virtual como Wikipédia?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações em sites de enciclopédia virtual como Wikipédia?'
        NAO = MetaValue(0.0, 'C8_E')
        SIM = MetaValue(1.0, 'C8_E')
        NAO_SABE = MetaValue(97.0, 'C8_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_F:
        """Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações oferecidas por sites de governo?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para procurar informações oferecidas por sites de governo?'
        NAO = MetaValue(0.0, 'C8_F')
        SIM = MetaValue(1.0, 'C8_F')
        NAO_SABE = MetaValue(97.0, 'C8_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_G:
        """Nos últimos 3 meses, o respondente utilizou a Internet para realizar algum serviço público como, por exemplo, emitir documentos pela Internet, preencher e enviar formulários online, ou pagar taxas e impostos pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para realizar algum serviço público como, por exemplo, emitir documentos pela Internet, preencher e enviar formulários online, ou pagar taxas e impostos pela Internet?'
        NAO = MetaValue(0.0, 'C8_G')
        SIM = MetaValue(1.0, 'C8_G')
        NAO_SABE = MetaValue(97.0, 'C8_G')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_H:
        """Nos últimos 3 meses, o respondente utilizou a Internet para fazer consultas, pagamentos ou outras transações financeiras?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para fazer consultas, pagamentos ou outras transações financeiras?'
        NAO = MetaValue(0.0, 'C8_H')
        SIM = MetaValue(1.0, 'C8_H')
        NAO_SABE = MetaValue(97.0, 'C8_H')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_H')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C8_I:
        """Nos últimos 3 meses, o respondente utilizou a Internet para fazer pagamento ou transferência por Pix?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para fazer pagamento ou transferência por Pix?'
        NAO = MetaValue(0.0, 'C8_I')
        SIM = MetaValue(1.0, 'C8_I')
        NAO_SABE = MetaValue(97.0, 'C8_I')
        NAO_RESPONDEU = MetaValue(98.0, 'C8_I')
        NAO_SE_APLICA = MetaValue(99.0, 'C8_I')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet para jogar on-line?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para jogar on-line?'
        NAO = MetaValue(0.0, 'C9_A')
        SIM = MetaValue(1.0, 'C9_A')
        NAO_SABE = MetaValue(97.0, 'C9_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet para ouvir música on-line como por Spotify, por Deezer ou por Youtube?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para ouvir música on-line como por Spotify, por Deezer ou por Youtube?'
        NAO = MetaValue(0.0, 'C9_B')
        SIM = MetaValue(1.0, 'C9_B')
        NAO_SABE = MetaValue(97.0, 'C9_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet para assistir vídeos, programas, filmes ou séries em sites como o Youtube ou Netflix?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para assistir vídeos, programas, filmes ou séries em sites como o Youtube ou Netflix?'
        NAO = MetaValue(0.0, 'C9_C')
        SIM = MetaValue(1.0, 'C9_C')
        NAO_SABE = MetaValue(97.0, 'C9_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_D:
        """Nos últimos 3 meses, o respondente utilizou a Internet para ler jornais, revistas ou notícias?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para ler jornais, revistas ou notícias?'
        NAO = MetaValue(0.0, 'C9_D')
        SIM = MetaValue(1.0, 'C9_D')
        NAO_SABE = MetaValue(97.0, 'C9_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_F:
        """Nos últimos 3 meses, o respondente utilizou a Internet para ver exposições e museus?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para ver exposições e museus?'
        NAO = MetaValue(0.0, 'C9_F')
        SIM = MetaValue(1.0, 'C9_F')
        NAO_SABE = MetaValue(97.0, 'C9_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_G:
        """Nos últimos 3 meses, o respondente utilizou a Internet para ouvir podcasts?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para ouvir podcasts?'
        NAO = MetaValue(0.0, 'C9_G')
        SIM = MetaValue(1.0, 'C9_G')
        NAO_SABE = MetaValue(97.0, 'C9_G')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C9_E:
        """Nos últimos 3 meses, o respondente utilizou a Internet para acompanhar transmissões de áudio ou vídeo em tempo real ou lives pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para acompanhar transmissões de áudio ou vídeo em tempo real ou lives pela Internet?'
        NAO = MetaValue(0.0, 'C9_E')
        SIM = MetaValue(1.0, 'C9_E')
        NAO_SABE = MetaValue(97.0, 'C9_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C9_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C9_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet para realizar atividades ou pesquisas escolares?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para realizar atividades ou pesquisas escolares?'
        NAO = MetaValue(0.0, 'C10_A')
        SIM = MetaValue(1.0, 'C10_A')
        NAO_SABE = MetaValue(97.0, 'C10_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet para fazer cursos à distância?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para fazer cursos à distância?'
        NAO = MetaValue(0.0, 'C10_B')
        SIM = MetaValue(1.0, 'C10_B')
        NAO_SABE = MetaValue(97.0, 'C10_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet para buscar informações sobre cursos de graduação, pós-graduação e de extensão?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para buscar informações sobre cursos de graduação, pós-graduação e de extensão?'
        NAO = MetaValue(0.0, 'C10_C')
        SIM = MetaValue(1.0, 'C10_C')
        NAO_SABE = MetaValue(97.0, 'C10_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_D:
        """Nos últimos 3 meses, o respondente utilizou a Internet para estudar na Internet por conta própria?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para estudar na Internet por conta própria?'
        NAO = MetaValue(0.0, 'C10_D')
        SIM = MetaValue(1.0, 'C10_D')
        NAO_SABE = MetaValue(97.0, 'C10_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_E:
        """Nos últimos 3 meses, o respondente utilizou a Internet para usar serviço de armazenamento na Internet, como por exemplo Dropbox, Google Drive, Onedrive?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para usar serviço de armazenamento na Internet, como por exemplo Dropbox, Google Drive, Onedrive?'
        NAO = MetaValue(0.0, 'C10_E')
        SIM = MetaValue(1.0, 'C10_E')
        NAO_SABE = MetaValue(97.0, 'C10_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C10_F:
        """Nos últimos 3 meses, o respondente utilizou a Internet para realizar atividades de trabalho?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para realizar atividades de trabalho?'
        NAO = MetaValue(0.0, 'C10_F')
        SIM = MetaValue(1.0, 'C10_F')
        NAO_SABE = MetaValue(97.0, 'C10_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C10_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C10_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C11_A:
        """Nos últimos 3 meses, o respondente utilizou a Internet para compartilhar conteúdo na Internet, como textos, imagens, fotos, vídeos ou músicas?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para compartilhar conteúdo na Internet, como textos, imagens, fotos, vídeos ou músicas?'
        NAO = MetaValue(0.0, 'C11_A')
        SIM = MetaValue(1.0, 'C11_A')
        NAO_SABE = MetaValue(97.0, 'C11_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C11_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C11_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C11_B:
        """Nos últimos 3 meses, o respondente utilizou a Internet para criar ou atualizar blogs, páginas na Internet ou websites?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para criar ou atualizar blogs, páginas na Internet ou websites?'
        NAO = MetaValue(0.0, 'C11_B')
        SIM = MetaValue(1.0, 'C11_B')
        NAO_SABE = MetaValue(97.0, 'C11_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C11_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C11_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C11_C:
        """Nos últimos 3 meses, o respondente utilizou a Internet para postar na Internet textos, imagens, fotos, vídeos ou músicas que o respondente mesmo fez?"""
        _label = 'Nos últimos 3 meses, o respondente utilizou a Internet para postar na Internet textos, imagens, fotos, vídeos ou músicas que o respondente mesmo fez?'
        NAO = MetaValue(0.0, 'C11_C')
        SIM = MetaValue(1.0, 'C11_C')
        NAO_SABE = MetaValue(97.0, 'C11_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C11_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C11_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13A:
        """Nos últimos 3 meses, o(a) sr.(a) usou ferramenta de inteligência artificial, como chatGPT, Copilot, Gemini ou a Meta IA do WhatsApp?"""
        _label = 'Nos últimos 3 meses, o(a) sr.(a) usou ferramenta de inteligência artificial, como chatGPT, Copilot, Gemini ou a Meta IA do WhatsApp?'
        NAO = MetaValue(0.0, 'C13A')
        SIM = MetaValue(1.0, 'C13A')
        NAO_SABE = MetaValue(97.0, 'C13A')
        NAO_RESPONDEU = MetaValue(98.0, 'C13A')
        NAO_SE_APLICA = MetaValue(99.0, 'C13A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13B_A:
        """E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para uso profissional ou de trabalho"""
        _label = 'E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para uso profissional ou de trabalho'
        NAO = MetaValue(0.0, 'C13B_A')
        SIM = MetaValue(1.0, 'C13B_A')
        NAO_SABE = MetaValue(97.0, 'C13B_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C13B_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C13B_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13B_B:
        """E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para pesquisa ou trabalho escolar ou da faculdade"""
        _label = 'E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para pesquisa ou trabalho escolar ou da faculdade'
        NAO = MetaValue(0.0, 'C13B_B')
        SIM = MetaValue(1.0, 'C13B_B')
        NAO_SABE = MetaValue(97.0, 'C13B_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C13B_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C13B_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13B_C:
        """E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para uso pessoal"""
        _label = 'E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para uso pessoal'
        NAO = MetaValue(0.0, 'C13B_C')
        SIM = MetaValue(1.0, 'C13B_C')
        NAO_SABE = MetaValue(97.0, 'C13B_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C13B_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C13B_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13B_OUTRO:
        """E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para outra finalidade"""
        _label = 'E para que finalidade o(a) sr.(a) usou uma ferramenta de inteligência artificial nos últimos 3 meses? Para outra finalidade'
        NAO = MetaValue(0.0, 'C13B_OUTRO')
        SIM = MetaValue(1.0, 'C13B_OUTRO')
        NAO_SABE = MetaValue(97.0, 'C13B_OUTRO')
        NAO_RESPONDEU = MetaValue(98.0, 'C13B_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C13B_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13C_A:
        """E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de interesse ou necessidade"""
        _label = 'E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de interesse ou necessidade'
        NAO = MetaValue(0.0, 'C13C_A')
        SIM = MetaValue(1.0, 'C13C_A')
        NAO_SABE = MetaValue(97.0, 'C13C_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C13C_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C13C_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13C_B:
        """E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de conhecimento da existência desse tipo de ferramenta"""
        _label = 'E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de conhecimento da existência desse tipo de ferramenta'
        NAO = MetaValue(0.0, 'C13C_B')
        SIM = MetaValue(1.0, 'C13C_B')
        NAO_SABE = MetaValue(97.0, 'C13C_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C13C_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C13C_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13C_C:
        """E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de habilidade para usar esse tipo de ferramenta"""
        _label = 'E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por falta de habilidade para usar esse tipo de ferramenta'
        NAO = MetaValue(0.0, 'C13C_C')
        SIM = MetaValue(1.0, 'C13C_C')
        NAO_SABE = MetaValue(97.0, 'C13C_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C13C_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C13C_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13C_D:
        """E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por ter preocupações com segurança ou privacidade"""
        _label = 'E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por ter preocupações com segurança ou privacidade'
        NAO = MetaValue(0.0, 'C13C_D')
        SIM = MetaValue(1.0, 'C13C_D')
        NAO_SABE = MetaValue(97.0, 'C13C_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C13C_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C13C_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C13C_OUTRO:
        """E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por outro motivo"""
        _label = 'E por quais motivos o(a) sr.(a) não usou ferramenta de inteligência artificial nos últimos 3 meses? Por outro motivo'
        NAO = MetaValue(0.0, 'C13C_OUTRO')
        SIM = MetaValue(1.0, 'C13C_OUTRO')
        NAO_SABE = MetaValue(97.0, 'C13C_OUTRO')
        NAO_RESPONDEU = MetaValue(98.0, 'C13C_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C13C_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C14_A:
        """E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta em loteria federal, como Mega Sena, Lotofácil ou Loteca"""
        _label = 'E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta em loteria federal, como Mega Sena, Lotofácil ou Loteca'
        NAO = MetaValue(0.0, 'C14_A')
        SIM = MetaValue(1.0, 'C14_A')
        NAO_SABE = MetaValue(97.0, 'C14_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C14_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C14_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C14_B:
        """E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta em cassino online, como o jogo do tigrinho"""
        _label = 'E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta em cassino online, como o jogo do tigrinho'
        NAO = MetaValue(0.0, 'C14_B')
        SIM = MetaValue(1.0, 'C14_B')
        NAO_SABE = MetaValue(97.0, 'C14_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C14_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C14_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C14_C:
        """E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta esportiva, por sites ou aplicativos como Superbet, Bet365 ou Betano"""
        _label = 'E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Fez aposta esportiva, por sites ou aplicativos como Superbet, Bet365 ou Betano'
        NAO = MetaValue(0.0, 'C14_C')
        SIM = MetaValue(1.0, 'C14_C')
        NAO_SABE = MetaValue(97.0, 'C14_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C14_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C14_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C14_D:
        """E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Pagou para participar de uma rifa digital ou de algum sorteio divulgado em uma rede social ou em aplicativo de mensagem"""
        _label = 'E quais das seguintes atividades o(a) sr.(a) realizou na Internet nos últimos 3 meses? Pagou para participar de uma rifa digital ou de algum sorteio divulgado em uma rede social ou em aplicativo de mensagem'
        NAO = MetaValue(0.0, 'C14_D')
        SIM = MetaValue(1.0, 'C14_D')
        NAO_SABE = MetaValue(97.0, 'C14_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C14_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C14_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class H2:
        """Nos últimos 12 meses, o respondente comprou ou encomendou produtos ou serviços pela Internet, mesmo que o pagamento não tenha sido feito pela Internet?"""
        _label = 'Nos últimos 12 meses, o respondente comprou ou encomendou produtos ou serviços pela Internet, mesmo que o pagamento não tenha sido feito pela Internet?'
        NAO = MetaValue(0.0, 'H2')
        SIM = MetaValue(1.0, 'H2')
        NAO_SABE = MetaValue(97.0, 'H2')
        NAO_RESPONDEU = MetaValue(98.0, 'H2')
        NAO_SE_APLICA = MetaValue(99.0, 'H2')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B1:
        """O respondente já usou um computador de mesa, um notebook ou um tablet?"""
        _label = 'O respondente já usou um computador de mesa, um notebook ou um tablet?'
        SIM = MetaValue(1.0, 'B1')
        NAO = MetaValue(0.0, 'B1')
        NAO_SABE = MetaValue(97.0, 'B1')
        NAO_RESPONDEU = MetaValue(98.0, 'B1')
        _map = {1.0: 'Sim', 0.0: 'Não', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class B2:
        """Quando o respondente usou um computador de mesa, um notebook ou um tablet pela última vez?"""
        _label = 'Quando o respondente usou um computador de mesa, um notebook ou um tablet pela última vez?'
        HA_MENOS_DE_TRES_MESES_USUARIO1 = MetaValue(1.0, 'B2')
        ENTRE_TRES_E_DOZE_MESES_ATRAS = MetaValue(2.0, 'B2')
        MAIS_DE_DOZE_MESES_ATRAS = MetaValue(3.0, 'B2')
        NUNCA_USOU_UM_COMPUTADOR = MetaValue(99.0, 'B2')
        _map = {1.0: 'Há menos de três meses (usuário)¹', 2.0: 'Entre três e doze meses atrás', 3.0: 'Mais de doze meses atrás', 99.0: 'Nunca usou um computador'}

    class B4_A:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet em casa?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet em casa?'
        NAO = MetaValue(0.0, 'B4_A')
        SIM = MetaValue(1.0, 'B4_A')
        NAO_SABE = MetaValue(97.0, 'B4_A')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_A')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_B1:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no local de trabalho, sem contar sua própria casa?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no local de trabalho, sem contar sua própria casa?'
        NAO = MetaValue(0.0, 'B4_B1')
        SIM = MetaValue(1.0, 'B4_B1')
        NAO_SABE = MetaValue(97.0, 'B4_B1')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_B1')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_B1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_C:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet na escola ou estabelecimento de ensino?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet na escola ou estabelecimento de ensino?'
        NAO = MetaValue(0.0, 'B4_C')
        SIM = MetaValue(1.0, 'B4_C')
        NAO_SABE = MetaValue(97.0, 'B4_C')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_C')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_D:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?'
        NAO = MetaValue(0.0, 'B4_D')
        SIM = MetaValue(1.0, 'B4_D')
        NAO_SABE = MetaValue(97.0, 'B4_D')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_D')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_E:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?'
        NAO = MetaValue(0.0, 'B4_E')
        SIM = MetaValue(1.0, 'B4_E')
        NAO_SABE = MetaValue(97.0, 'B4_E')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_E')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_F:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou  Internet Café?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou  Internet Café?'
        NAO = MetaValue(0.0, 'B4_F')
        SIM = MetaValue(1.0, 'B4_F')
        NAO_SABE = MetaValue(97.0, 'B4_F')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_F')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_G:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet enquanto se desloca, como por exemplo na rua, no ônibus, no metrô ou no carro?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet enquanto se desloca, como por exemplo na rua, no ônibus, no metrô ou no carro?'
        NAO = MetaValue(0.0, 'B4_G')
        SIM = MetaValue(1.0, 'B4_G')
        NAO_SABE = MetaValue(97.0, 'B4_G')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_G')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class B4_H:
        """Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet em algum outro lugar?"""
        _label = 'Nos últimos 3 meses, o respondente usou um computador de mesa, um notebook ou um tablet em algum outro lugar?'
        NAO = MetaValue(0.0, 'B4_H')
        SIM = MetaValue(1.0, 'B4_H')
        NAO_SABE = MetaValue(97.0, 'B4_H')
        NAO_RESPONDEU = MetaValue(98.0, 'B4_H')
        NAO_SE_APLICA = MetaValue(99.0, 'B4_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_A:
        """Nos últimos 3 meses, o respondente copiou ou moveu um arquivo ou uma pasta, por exemplo, em um computador ou na nuvem?"""
        _label = 'Nos últimos 3 meses, o respondente copiou ou moveu um arquivo ou uma pasta, por exemplo, em um computador ou na nuvem?'
        NAO = MetaValue(0.0, 'I1A_A')
        SIM = MetaValue(1.0, 'I1A_A')
        NAO_SABE = MetaValue(97.0, 'I1A_A')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_A')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_B:
        """Nos últimos 3 meses, o respondente usou ferramenta de copiar e colar para duplicar ou mover conteúdo, por exemplo, em um documento ou uma mensagem?"""
        _label = 'Nos últimos 3 meses, o respondente usou ferramenta de copiar e colar para duplicar ou mover conteúdo, por exemplo, em um documento ou uma mensagem?'
        NAO = MetaValue(0.0, 'I1A_B')
        SIM = MetaValue(1.0, 'I1A_B')
        NAO_SABE = MetaValue(97.0, 'I1A_B')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_B')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_C:
        """Nos últimos 3 meses, o respondente anexou documento, imagem ou vídeo a mensagens instantâneas, e-mails ou SMS?"""
        _label = 'Nos últimos 3 meses, o respondente anexou documento, imagem ou vídeo a mensagens instantâneas, e-mails ou SMS?'
        NAO = MetaValue(0.0, 'I1A_C')
        SIM = MetaValue(1.0, 'I1A_C')
        NAO_SABE = MetaValue(97.0, 'I1A_C')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_C')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_D:
        """Nos últimos 3 meses, o respondente usou fórmula em uma planilha de cálculo?"""
        _label = 'Nos últimos 3 meses, o respondente usou fórmula em uma planilha de cálculo?'
        NAO = MetaValue(0.0, 'I1A_D')
        SIM = MetaValue(1.0, 'I1A_D')
        NAO_SABE = MetaValue(97.0, 'I1A_D')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_D')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_E:
        """Nos últimos 3 meses, o respondente conectou ou instalou novos equipamentos com ou sem fio, como modem, impressora, câmera ou microfone?"""
        _label = 'Nos últimos 3 meses, o respondente conectou ou instalou novos equipamentos com ou sem fio, como modem, impressora, câmera ou microfone?'
        NAO = MetaValue(0.0, 'I1A_E')
        SIM = MetaValue(1.0, 'I1A_E')
        NAO_SABE = MetaValue(97.0, 'I1A_E')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_E')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_F:
        """Nos últimos 3 meses, o respondente instalou programas de computador ou aplicativos de celular?"""
        _label = 'Nos últimos 3 meses, o respondente instalou programas de computador ou aplicativos de celular?'
        NAO = MetaValue(0.0, 'I1A_F')
        SIM = MetaValue(1.0, 'I1A_F')
        NAO_SABE = MetaValue(97.0, 'I1A_F')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_F')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_G:
        """Nos últimos 3 meses, o respondente criou uma apresentação de slides?"""
        _label = 'Nos últimos 3 meses, o respondente criou uma apresentação de slides?'
        NAO = MetaValue(0.0, 'I1A_G')
        SIM = MetaValue(1.0, 'I1A_G')
        NAO_SABE = MetaValue(97.0, 'I1A_G')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_G')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_H:
        """Nos últimos 3 meses, o respondente transferiu arquivos ou aplicativos entre dispositivos, inclusive pela nuvem?"""
        _label = 'Nos últimos 3 meses, o respondente transferiu arquivos ou aplicativos entre dispositivos, inclusive pela nuvem?'
        NAO = MetaValue(0.0, 'I1A_H')
        SIM = MetaValue(1.0, 'I1A_H')
        NAO_SABE = MetaValue(97.0, 'I1A_H')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_H')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_I:
        """Nos últimos 3 meses, o respondente criou programa de computador ou aplicativo de celular usando linguagem de programação?"""
        _label = 'Nos últimos 3 meses, o respondente criou programa de computador ou aplicativo de celular usando linguagem de programação?'
        NAO = MetaValue(0.0, 'I1A_I')
        SIM = MetaValue(1.0, 'I1A_I')
        NAO_SABE = MetaValue(97.0, 'I1A_I')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_I')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_I')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_J:
        """Nos últimos 3 meses, o respondente adotou medidas de segurança, como senhas fortes ou verificação em duas etapas, para proteger dispositivos e contas online?"""
        _label = 'Nos últimos 3 meses, o respondente adotou medidas de segurança, como senhas fortes ou verificação em duas etapas, para proteger dispositivos e contas online?'
        NAO = MetaValue(0.0, 'I1A_J')
        SIM = MetaValue(1.0, 'I1A_J')
        NAO_SABE = MetaValue(97.0, 'I1A_J')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_J')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_J')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_K:
        """Nos últimos 3 meses, o respondente mudou configurações de privacidade no seu dispositivo, conta ou aplicativo para limitar o compartilhamento de dados pessoais, como seu nome, contato ou foto?"""
        _label = 'Nos últimos 3 meses, o respondente mudou configurações de privacidade no seu dispositivo, conta ou aplicativo para limitar o compartilhamento de dados pessoais, como seu nome, contato ou foto?'
        NAO = MetaValue(0.0, 'I1A_K')
        SIM = MetaValue(1.0, 'I1A_K')
        NAO_SABE = MetaValue(97.0, 'I1A_K')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_K')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_K')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class I1A_L:
        """Nos últimos 3 meses, o respondente verificou se uma informação que encontrou na Internet era verdadeira?"""
        _label = 'Nos últimos 3 meses, o respondente verificou se uma informação que encontrou na Internet era verdadeira?'
        NAO = MetaValue(0.0, 'I1A_L')
        SIM = MetaValue(1.0, 'I1A_L')
        NAO_SABE = MetaValue(97.0, 'I1A_L')
        NAO_RESPONDEU = MetaValue(98.0, 'I1A_L')
        NAO_SE_APLICA = MetaValue(99.0, 'I1A_L')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J1:
        """Nos últimos 3 meses, o respondente usou um telefone celular?"""
        _label = 'Nos últimos 3 meses, o respondente usou um telefone celular?'
        NAO = MetaValue(0.0, 'J1')
        SIM = MetaValue(1.0, 'J1')
        NAO_SABE = MetaValue(97.0, 'J1')
        NAO_RESPONDEU = MetaValue(98.0, 'J1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class J2_A:
        """Nos últimos 3 meses, o respondente usou o telefone celular para efetuar e receber chamadas telefônicas?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para efetuar e receber chamadas telefônicas?'
        NAO = MetaValue(0.0, 'J2_A')
        SIM = MetaValue(1.0, 'J2_A')
        NAO_SABE = MetaValue(97.0, 'J2_A')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_A')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_B:
        """Nos últimos 3 meses, o respondente usou o telefone celular para enviar mensagens de texto SMS?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para enviar mensagens de texto SMS?'
        NAO = MetaValue(0.0, 'J2_B')
        SIM = MetaValue(1.0, 'J2_B')
        NAO_SABE = MetaValue(97.0, 'J2_B')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_B')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_C:
        """Nos últimos 3 meses, o respondente usou o telefone celular para ouvir músicas?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para ouvir músicas?'
        NAO = MetaValue(0.0, 'J2_C')
        SIM = MetaValue(1.0, 'J2_C')
        NAO_SABE = MetaValue(97.0, 'J2_C')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_C')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_D:
        """Nos últimos 3 meses, o respondente usou o telefone celular para assistir vídeos?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para assistir vídeos?'
        NAO = MetaValue(0.0, 'J2_D')
        SIM = MetaValue(1.0, 'J2_D')
        NAO_SABE = MetaValue(97.0, 'J2_D')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_D')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_E:
        """Nos últimos 3 meses, o respondente usou o telefone celular para jogar?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para jogar?'
        NAO = MetaValue(0.0, 'J2_E')
        SIM = MetaValue(1.0, 'J2_E')
        NAO_SABE = MetaValue(97.0, 'J2_E')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_E')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_F:
        """Nos últimos 3 meses, o respondente usou o telefone celular para tirar fotos?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para tirar fotos?'
        NAO = MetaValue(0.0, 'J2_F')
        SIM = MetaValue(1.0, 'J2_F')
        NAO_SABE = MetaValue(97.0, 'J2_F')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_F')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_G:
        """Nos últimos 3 meses, o respondente usou o telefone celular para usar mapas, por exemplo o Google Maps?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para usar mapas, por exemplo o Google Maps?'
        NAO = MetaValue(0.0, 'J2_G')
        SIM = MetaValue(1.0, 'J2_G')
        NAO_SABE = MetaValue(97.0, 'J2_G')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_G')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_H1:
        """Nos últimos 3 meses, o respondente usou o telefone celular para enviar e receber e-mails?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para enviar e receber e-mails?'
        NAO = MetaValue(0.0, 'J2_H1')
        SIM = MetaValue(1.0, 'J2_H1')
        NAO_SABE = MetaValue(97.0, 'J2_H1')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_H1')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_H1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_I1:
        """Nos últimos 3 meses, o respondente usou o telefone celular para acessar redes sociais, como Facebook, Instagram ou TikTok?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para acessar redes sociais, como Facebook, Instagram ou TikTok?'
        NAO = MetaValue(0.0, 'J2_I1')
        SIM = MetaValue(1.0, 'J2_I1')
        NAO_SABE = MetaValue(97.0, 'J2_I1')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_I1')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_I1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_J:
        """Nos últimos 3 meses, o respondente usou o telefone celular para acessar páginas ou sites?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para acessar páginas ou sites?'
        NAO = MetaValue(0.0, 'J2_J')
        SIM = MetaValue(1.0, 'J2_J')
        NAO_SABE = MetaValue(97.0, 'J2_J')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_J')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_J')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_K:
        """Nos últimos 3 meses, o respondente usou o telefone celular para baixar aplicativos?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para baixar aplicativos?'
        NAO = MetaValue(0.0, 'J2_K')
        SIM = MetaValue(1.0, 'J2_K')
        NAO_SABE = MetaValue(97.0, 'J2_K')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_K')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_K')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_L:
        """Nos últimos 3 meses, o respondente usou o telefone celular para buscar informações, como por exemplo no Google?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para buscar informações, como por exemplo no Google?'
        NAO = MetaValue(0.0, 'J2_L')
        SIM = MetaValue(1.0, 'J2_L')
        NAO_SABE = MetaValue(97.0, 'J2_L')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_L')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_L')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_M:
        """Nos últimos 3 meses, o respondente usou o telefone celular para compartilhar fotos, vídeos ou textos?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para compartilhar fotos, vídeos ou textos?'
        NAO = MetaValue(0.0, 'J2_M')
        SIM = MetaValue(1.0, 'J2_M')
        NAO_SABE = MetaValue(97.0, 'J2_M')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_M')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_M')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_N:
        """Nos últimos 3 meses, o respondente usou o telefone celular para enviar mensagens de texto pela Internet, como por WhatsApp, Skype ou chat do Facebook?"""
        _label = 'Nos últimos 3 meses, o respondente usou o telefone celular para enviar mensagens de texto pela Internet, como por WhatsApp, Skype ou chat do Facebook?'
        NAO = MetaValue(0.0, 'J2_N')
        SIM = MetaValue(1.0, 'J2_N')
        NAO_SABE = MetaValue(97.0, 'J2_N')
        NAO_RESPONDEU = MetaValue(98.0, 'J2_N')
        NAO_SE_APLICA = MetaValue(99.0, 'J2_N')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J3:
        """O respondente usou a Internet pelo telefone celular nos últimos 3 meses?"""
        _label = 'O respondente usou a Internet pelo telefone celular nos últimos 3 meses?'
        NAO = MetaValue(0.0, 'J3')
        SIM = MetaValue(1.0, 'J3')
        NAO_SABE = MetaValue(97.0, 'J3')
        NAO_RESPONDEU = MetaValue(98.0, 'J3')
        NAO_SE_APLICA = MetaValue(99.0, 'J3')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J3A_A:
        """Quando o respondente usou a Internet pelo telefone celular nos últimos 3 meses, utilizou conexão 3g ou 4g?"""
        _label = 'Quando o respondente usou a Internet pelo telefone celular nos últimos 3 meses, utilizou conexão 3g ou 4g?'
        NAO = MetaValue(0.0, 'J3A_A')
        SIM = MetaValue(1.0, 'J3A_A')
        NAO_SABE = MetaValue(97.0, 'J3A_A')
        NAO_RESPONDEU = MetaValue(98.0, 'J3A_A')
        NAO_SE_APLICA = MetaValue(99.0, 'J3A_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J3A_B:
        """Quando o respondente usou a Internet pelo telefone celular nos últimos 3 meses, utilizou conexão wi-fi?"""
        _label = 'Quando o respondente usou a Internet pelo telefone celular nos últimos 3 meses, utilizou conexão wi-fi?'
        NAO = MetaValue(0.0, 'J3A_B')
        SIM = MetaValue(1.0, 'J3A_B')
        NAO_SABE = MetaValue(97.0, 'J3A_B')
        NAO_RESPONDEU = MetaValue(98.0, 'J3A_B')
        NAO_SE_APLICA = MetaValue(99.0, 'J3A_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J5:
        """O respondente possui telefone celular?"""
        _label = 'O respondente possui telefone celular?'
        NAO = MetaValue(0.0, 'J5')
        SIM = MetaValue(1.0, 'J5')
        NAO_SABE = MetaValue(97.0, 'J5')
        NAO_RESPONDEU = MetaValue(98.0, 'J5')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class J5_QTD_LINHAS:
        """Quantidade de linhas/chips ativos informados pelo respondente."""
        _label = 'Quantidade de linhas/chips ativos informados pelo respondente.'
        NAO_SE_APLICA = MetaValue(99.0, 'J5_QTD_LINHAS')
        _map = {99.0: 'Não se aplica'}

    class J6:
        """O telefone que o respondente possui é pré ou pós pago?"""
        _label = 'O telefone que o respondente possui é pré ou pós pago?'
        PRE_PAGO = MetaValue(1.0, 'J6')
        POS_PAGO = MetaValue(2.0, 'J6')
        CONTROLE = MetaValue(3.0, 'J6')
        NAO_SABE = MetaValue(97.0, 'J6')
        NAO_RESPONDEU = MetaValue(98.0, 'J6')
        NAO_SE_APLICA = MetaValue(99.0, 'J6')
        _map = {1.0: 'Pré-Pago', 2.0: 'Pós-Pago', 3.0: 'Controle', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J7:
        """Em algum momento nos últimos três meses, o seu pacote de dados do celular acabou?"""
        _label = 'Em algum momento nos últimos três meses, o seu pacote de dados do celular acabou?'
        NAO = MetaValue(0.0, 'J7')
        SIM = MetaValue(1.0, 'J7')
        NAO_SABE = MetaValue(97.0, 'J7')
        NAO_RESPONDEU = MetaValue(98.0, 'J7')
        NAO_SE_APLICA = MetaValue(99.0, 'J7')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J8A:
        """Na última vez em que seu pacote de dados acabou, o(a) sr.(a)... ?"""
        _label = 'Na última vez em que seu pacote de dados acabou, o(a) sr.(a)... ?'
        CONSEGUIU_USAR_TODOS_OS_APLICATIVOS_QUE_COSTUMAVA_USAR = MetaValue(1.0, 'J8A')
        SO_CONSEGUIU_USAR_ALGUNS_DOS_APLICATIVOS_QUE_COSTUMAVA_USAR = MetaValue(2.0, 'J8A')
        NAO_CONSEGUIU_USAR_NENHUM_DOS_APLICATIVOS_QUE_COSTUMAVA_USAR = MetaValue(3.0, 'J8A')
        NAO_SE_APLICA = MetaValue(99.0, 'J8A')
        _map = {1.0: 'Conseguiu usar todos os aplicativos que costumava usar', 2.0: 'Só conseguiu usar alguns dos aplicativos que costumava usar', 3.0: 'Não conseguiu usar nenhum dos aplicativos que costumava usar', 99.0: 'Não se aplica'}

    class J8B_C:
        """E na última vez em que seu pacote de dados acabou, quais das seguintes situações aconteceram com o(a) sr.(a)? A velocidade da Internet no seu celular foi reduzida"""
        _label = 'E na última vez em que seu pacote de dados acabou, quais das seguintes situações aconteceram com o(a) sr.(a)? A velocidade da Internet no seu celular foi reduzida'
        NAO = MetaValue(0.0, 'J8B_C')
        SIM = MetaValue(1.0, 'J8B_C')
        NAO_SABE = MetaValue(97.0, 'J8B_C')
        NAO_RESPONDEU = MetaValue(98.0, 'J8B_C')
        NAO_SE_APLICA = MetaValue(99.0, 'J8B_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J8B_D:
        """E na última vez em que seu pacote de dados acabou, quais das seguintes situações aconteceram com o(a) sr.(a)? O(A) sr(a) teve que colocar mais créditos ou contratar um pacote adicional para continuar usando a Internet no telefone celular"""
        _label = 'E na última vez em que seu pacote de dados acabou, quais das seguintes situações aconteceram com o(a) sr.(a)? O(A) sr(a) teve que colocar mais créditos ou contratar um pacote adicional para continuar usando a Internet no telefone celular'
        NAO = MetaValue(0.0, 'J8B_D')
        SIM = MetaValue(1.0, 'J8B_D')
        NAO_SABE = MetaValue(97.0, 'J8B_D')
        NAO_RESPONDEU = MetaValue(98.0, 'J8B_D')
        NAO_SE_APLICA = MetaValue(99.0, 'J8B_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_A:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos de compartilhamento de vídeos, como Youtube ou Vimeo?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos de compartilhamento de vídeos, como Youtube ou Vimeo?'
        NAO = MetaValue(0.0, 'TC2B_A')
        SIM = MetaValue(1.0, 'TC2B_A')
        NAO_SABE = MetaValue(97.0, 'TC2B_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_B:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços por assinatura, como Spotify, Deezer ou Amazon Music?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços por assinatura, como Spotify, Deezer ou Amazon Music?'
        NAO = MetaValue(0.0, 'TC2B_B')
        SIM = MetaValue(1.0, 'TC2B_B')
        NAO_SABE = MetaValue(97.0, 'TC2B_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_C:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços de compra de música, como iTunes?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços de compra de música, como iTunes?'
        NAO = MetaValue(0.0, 'TC2B_C')
        SIM = MetaValue(1.0, 'TC2B_C')
        NAO_SABE = MetaValue(97.0, 'TC2B_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_D:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços de download gratuito de conteúdos, como o 4Shared ou torrent?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em serviços de download gratuito de conteúdos, como o 4Shared ou torrent?'
        NAO = MetaValue(0.0, 'TC2B_D')
        SIM = MetaValue(1.0, 'TC2B_D')
        NAO_SABE = MetaValue(97.0, 'TC2B_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_E:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos de emissoras de rádio?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos de emissoras de rádio?'
        NAO = MetaValue(0.0, 'TC2B_E')
        SIM = MetaValue(1.0, 'TC2B_E')
        NAO_SABE = MetaValue(97.0, 'TC2B_E')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_E')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_F:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos com músicas gratuitas como Vagalume ou Soundcloud?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em sites ou aplicativos com músicas gratuitas como Vagalume ou Soundcloud?'
        NAO = MetaValue(0.0, 'TC2B_F')
        SIM = MetaValue(1.0, 'TC2B_F')
        NAO_SABE = MetaValue(97.0, 'TC2B_F')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_F')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC2B_G:
        """Nos últimos 3 meses, o respondente ouviu música pela Internet em outros sites ou aplicativos? (ESPONTÂNEA)"""
        _label = 'Nos últimos 3 meses, o respondente ouviu música pela Internet em outros sites ou aplicativos? (ESPONTÂNEA)'
        NAO = MetaValue(0.0, 'TC2B_G')
        SIM = MetaValue(1.0, 'TC2B_G')
        NAO_SABE = MetaValue(97.0, 'TC2B_G')
        NAO_RESPONDEU = MetaValue(98.0, 'TC2B_G')
        NAO_SE_APLICA = MetaValue(99.0, 'TC2B_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC3_A:
        """Nos últimos 3 meses, o respondente ouviu pela Internet músicas estrangeiras?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu pela Internet músicas estrangeiras?'
        NAO = MetaValue(0.0, 'TC3_A')
        SIM = MetaValue(1.0, 'TC3_A')
        NAO_SABE = MetaValue(97.0, 'TC3_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC3_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC3_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC3_B:
        """Nos últimos 3 meses, o respondente ouviu pela Internet músicas brasileiras?"""
        _label = 'Nos últimos 3 meses, o respondente ouviu pela Internet músicas brasileiras?'
        NAO = MetaValue(0.0, 'TC3_B')
        SIM = MetaValue(1.0, 'TC3_B')
        NAO_SABE = MetaValue(97.0, 'TC3_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC3_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC3_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4_A:
        """Nos últimos 3 meses, o respondentes assistiu filmes pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondentes assistiu filmes pela Internet?'
        NAO = MetaValue(0.0, 'TC4_A')
        SIM = MetaValue(1.0, 'TC4_A')
        NAO_SABE = MetaValue(97.0, 'TC4_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4_B:
        """Nos últimos 3 meses, o respondentes assistiu séries pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondentes assistiu séries pela Internet?'
        NAO = MetaValue(0.0, 'TC4_B')
        SIM = MetaValue(1.0, 'TC4_B')
        NAO_SABE = MetaValue(97.0, 'TC4_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4_C:
        """Nos últimos 3 meses, o respondentes assistiu a programas de TV pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondentes assistiu a programas de TV pela Internet?'
        NAO = MetaValue(0.0, 'TC4_C')
        SIM = MetaValue(1.0, 'TC4_C')
        NAO_SABE = MetaValue(97.0, 'TC4_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4_D:
        """Nos últimos 3 meses, o respondentes assistiua a outros vídeos pela Internet, como no Youtube, Facebook ou WhatsApp?"""
        _label = 'Nos últimos 3 meses, o respondentes assistiua a outros vídeos pela Internet, como no Youtube, Facebook ou WhatsApp?'
        NAO = MetaValue(0.0, 'TC4_D')
        SIM = MetaValue(1.0, 'TC4_D')
        NAO_SABE = MetaValue(97.0, 'TC4_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_A:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Notícias pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Notícias pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_A')
        SIM = MetaValue(1.0, 'TC4B_A')
        NAO_SABE = MetaValue(97.0, 'TC4B_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_B:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Esportes pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Esportes pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_B')
        SIM = MetaValue(1.0, 'TC4B_B')
        NAO_SABE = MetaValue(97.0, 'TC4B_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_C:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Música, como shows ou vídeo clipes pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Música, como shows ou vídeo clipes pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_C')
        SIM = MetaValue(1.0, 'TC4B_C')
        NAO_SABE = MetaValue(97.0, 'TC4B_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_D:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Comédia ou programas humorísticos pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Comédia ou programas humorísticos pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_D')
        SIM = MetaValue(1.0, 'TC4B_D')
        NAO_SABE = MetaValue(97.0, 'TC4B_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_E:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Eventos ou programas religiosos pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Eventos ou programas religiosos pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_E')
        SIM = MetaValue(1.0, 'TC4B_E')
        NAO_SABE = MetaValue(97.0, 'TC4B_E')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_E')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_K:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Culinária ou receitas pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Culinária ou receitas pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_K')
        SIM = MetaValue(1.0, 'TC4B_K')
        NAO_SABE = MetaValue(97.0, 'TC4B_K')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_K')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_K')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_L:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Cuidados pessoais, beleza ou saúde pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Cuidados pessoais, beleza ou saúde pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_L')
        SIM = MetaValue(1.0, 'TC4B_L')
        NAO_SABE = MetaValue(97.0, 'TC4B_L')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_L')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_L')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_F:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Animações ou desenhos animados pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Animações ou desenhos animados pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_F')
        SIM = MetaValue(1.0, 'TC4B_F')
        NAO_SABE = MetaValue(97.0, 'TC4B_F')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_F')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_G:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Pessoas jogando videogame pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Pessoas jogando videogame pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_G')
        SIM = MetaValue(1.0, 'TC4B_G')
        NAO_SABE = MetaValue(97.0, 'TC4B_G')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_G')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_H:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Tutoriais ou vídeo aulas pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Tutoriais ou vídeo aulas pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_H')
        SIM = MetaValue(1.0, 'TC4B_H')
        NAO_SABE = MetaValue(97.0, 'TC4B_H')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_H')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4B_I:
        """Nos últimos 3 meses, o respondente assistiu a vídeos de Influenciadores digitais, como youtubers pela Internet?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos de Influenciadores digitais, como youtubers pela Internet?'
        NAO = MetaValue(0.0, 'TC4B_I')
        SIM = MetaValue(1.0, 'TC4B_I')
        NAO_SABE = MetaValue(97.0, 'TC4B_I')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4B_I')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4B_I')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_A:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em sites ou aplicativos de compartilhamento de vídeos, como Youtube ou Vimeo?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em sites ou aplicativos de compartilhamento de vídeos, como Youtube ou Vimeo?'
        NAO = MetaValue(0.0, 'TC4C_A')
        SIM = MetaValue(1.0, 'TC4C_A')
        NAO_SABE = MetaValue(97.0, 'TC4C_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_B1:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em redes sociais, como Facebook, Instagram ou TikTok?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em redes sociais, como Facebook, Instagram ou TikTok?'
        NAO = MetaValue(0.0, 'TC4C_B1')
        SIM = MetaValue(1.0, 'TC4C_B1')
        NAO_SABE = MetaValue(97.0, 'TC4C_B1')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_B1')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_B1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_C:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em aplicativos de mensagens, como WhatsApp ou Telegram?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em aplicativos de mensagens, como WhatsApp ou Telegram?'
        NAO = MetaValue(0.0, 'TC4C_C')
        SIM = MetaValue(1.0, 'TC4C_C')
        NAO_SABE = MetaValue(97.0, 'TC4C_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_D1:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços por assinatura, como Netflix, Globoplay, Disney Plus ou Prime Video?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços por assinatura, como Netflix, Globoplay, Disney Plus ou Prime Video?'
        NAO = MetaValue(0.0, 'TC4C_D1')
        SIM = MetaValue(1.0, 'TC4C_D1')
        NAO_SABE = MetaValue(97.0, 'TC4C_D1')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_D1')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_D1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_E:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços de aluguel ou compra de vídeos, como Google Play  ou iTunes?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços de aluguel ou compra de vídeos, como Google Play  ou iTunes?'
        NAO = MetaValue(0.0, 'TC4C_E')
        SIM = MetaValue(1.0, 'TC4C_E')
        NAO_SABE = MetaValue(97.0, 'TC4C_E')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_E')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC4C_F:
        """Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços de download gratuito de conteúdos, como o 4Shared ou torrent?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu a vídeos, programas, filmes ou séries em serviços de download gratuito de conteúdos, como o 4Shared ou torrent?'
        NAO = MetaValue(0.0, 'TC4C_F')
        SIM = MetaValue(1.0, 'TC4C_F')
        NAO_SABE = MetaValue(97.0, 'TC4C_F')
        NAO_RESPONDEU = MetaValue(98.0, 'TC4C_F')
        NAO_SE_APLICA = MetaValue(99.0, 'TC4C_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC7_A:
        """Nos últimos 3 meses, o respondente assistiu pela Internet a filmes estrangeiros, ou seja, feitos em outros países?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu pela Internet a filmes estrangeiros, ou seja, feitos em outros países?'
        NAO = MetaValue(0.0, 'TC7_A')
        SIM = MetaValue(1.0, 'TC7_A')
        NAO_SABE = MetaValue(97.0, 'TC7_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC7_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC7_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC7_B:
        """Nos últimos 3 meses, o respondente assistiu pela Internet a filmes brasileiros, ou seja, feitos no Brasil?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu pela Internet a filmes brasileiros, ou seja, feitos no Brasil?'
        NAO = MetaValue(0.0, 'TC7_B')
        SIM = MetaValue(1.0, 'TC7_B')
        NAO_SABE = MetaValue(97.0, 'TC7_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC7_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC7_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC8_A:
        """Nos últimos 3 meses, o respondente assistiu pela Internet a séries estrangeiras, ou seja, feitas em outros países?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu pela Internet a séries estrangeiras, ou seja, feitas em outros países?'
        NAO = MetaValue(0.0, 'TC8_A')
        SIM = MetaValue(1.0, 'TC8_A')
        NAO_SABE = MetaValue(97.0, 'TC8_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC8_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC8_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC8_B:
        """Nos últimos 3 meses, o respondente assistiu pela Internet a séries brasileiras, ou seja, feitas no Brasil?"""
        _label = 'Nos últimos 3 meses, o respondente assistiu pela Internet a séries brasileiras, ou seja, feitas no Brasil?'
        NAO = MetaValue(0.0, 'TC8_B')
        SIM = MetaValue(1.0, 'TC8_B')
        NAO_SABE = MetaValue(97.0, 'TC8_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC8_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC8_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC10_A:
        """Nos últimos 3 meses, o respondente postou na Internet textos que criou?"""
        _label = 'Nos últimos 3 meses, o respondente postou na Internet textos que criou?'
        NAO = MetaValue(0.0, 'TC10_A')
        SIM = MetaValue(1.0, 'TC10_A')
        NAO_SABE = MetaValue(97.0, 'TC10_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC10_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC10_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC10_B:
        """Nos últimos 3 meses, o respondente postou na Internet imagens ou fotos que criou?"""
        _label = 'Nos últimos 3 meses, o respondente postou na Internet imagens ou fotos que criou?'
        NAO = MetaValue(0.0, 'TC10_B')
        SIM = MetaValue(1.0, 'TC10_B')
        NAO_SABE = MetaValue(97.0, 'TC10_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC10_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC10_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC10_C:
        """Nos últimos 3 meses, o respondente postou na Internet vídeos que criou?"""
        _label = 'Nos últimos 3 meses, o respondente postou na Internet vídeos que criou?'
        NAO = MetaValue(0.0, 'TC10_C')
        SIM = MetaValue(1.0, 'TC10_C')
        NAO_SABE = MetaValue(97.0, 'TC10_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC10_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC10_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC10_D:
        """Nos últimos 3 meses, o respondente postou na Internet músicas que criou?"""
        _label = 'Nos últimos 3 meses, o respondente postou na Internet músicas que criou?'
        NAO = MetaValue(0.0, 'TC10_D')
        SIM = MetaValue(1.0, 'TC10_D')
        NAO_SABE = MetaValue(97.0, 'TC10_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC10_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC10_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_A:
        """Nos últimos 3 meses, o respondente criou e postou na Internet fatos ou situações cotidianas?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet fatos ou situações cotidianas?'
        NAO = MetaValue(0.0, 'TC11_A')
        SIM = MetaValue(1.0, 'TC11_A')
        NAO_SABE = MetaValue(97.0, 'TC11_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_B:
        """Nos últimos 3 meses, o respondente criou e postou na Internet opinião sobre temas de seu interesse?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet opinião sobre temas de seu interesse?'
        NAO = MetaValue(0.0, 'TC11_B')
        SIM = MetaValue(1.0, 'TC11_B')
        NAO_SABE = MetaValue(97.0, 'TC11_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_C:
        """Nos últimos 3 meses, o respondente ensinou ou deu dicas pela internet para as pessoas sobre coisas que sabia?"""
        _label = 'Nos últimos 3 meses, o respondente ensinou ou deu dicas pela internet para as pessoas sobre coisas que sabia?'
        NAO = MetaValue(0.0, 'TC11_C')
        SIM = MetaValue(1.0, 'TC11_C')
        NAO_SABE = MetaValue(97.0, 'TC11_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_D:
        """Nos últimos 3 meses, o respondente criou e postou na Internet conteúdo artístico que criou?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet conteúdo artístico que criou?'
        NAO = MetaValue(0.0, 'TC11_D')
        SIM = MetaValue(1.0, 'TC11_D')
        NAO_SABE = MetaValue(97.0, 'TC11_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_E:
        """Nos últimos 3 meses, o respondente criou e postou na Internet para se tornar conhecido?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet para se tornar conhecido?'
        NAO = MetaValue(0.0, 'TC11_E')
        SIM = MetaValue(1.0, 'TC11_E')
        NAO_SABE = MetaValue(97.0, 'TC11_E')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_E')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_F:
        """Nos últimos 3 meses, o respondente criou e postou na Internet para se aproximar de pessoas com interesse comuns?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet para se aproximar de pessoas com interesse comuns?'
        NAO = MetaValue(0.0, 'TC11_F')
        SIM = MetaValue(1.0, 'TC11_F')
        NAO_SABE = MetaValue(97.0, 'TC11_F')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_F')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_G:
        """Nos últimos 3 meses, o respondente criou e postou na Internet para vender produtos ou serviços?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet para vender produtos ou serviços?'
        NAO = MetaValue(0.0, 'TC11_G')
        SIM = MetaValue(1.0, 'TC11_G')
        NAO_SABE = MetaValue(97.0, 'TC11_G')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_G')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC11_H:
        """Nos últimos 3 meses, o respondente criou e postou na Internet para divulgar seu trabalho?"""
        _label = 'Nos últimos 3 meses, o respondente criou e postou na Internet para divulgar seu trabalho?'
        NAO = MetaValue(0.0, 'TC11_H')
        SIM = MetaValue(1.0, 'TC11_H')
        NAO_SABE = MetaValue(97.0, 'TC11_H')
        NAO_RESPONDEU = MetaValue(98.0, 'TC11_H')
        NAO_SE_APLICA = MetaValue(99.0, 'TC11_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC12:
        """Nos últimos 3 meses, o respondente recebeu dinheiro ou outro tipo de pagamento pelo que criou ou postou na internet?"""
        _label = 'Nos últimos 3 meses, o respondente recebeu dinheiro ou outro tipo de pagamento pelo que criou ou postou na internet?'
        NAO = MetaValue(0.0, 'TC12')
        SIM = MetaValue(1.0, 'TC12')
        NAO_SABE = MetaValue(97.0, 'TC12')
        NAO_RESPONDEU = MetaValue(98.0, 'TC12')
        NAO_SE_APLICA = MetaValue(99.0, 'TC12')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_A:
        """O respondente procurou informações na internet para assistir a filmes no cinema?"""
        _label = 'O respondente procurou informações na internet para assistir a filmes no cinema?'
        NAO = MetaValue(0.0, 'TC13_A')
        SIM = MetaValue(1.0, 'TC13_A')
        NAO_SABE = MetaValue(97.0, 'TC13_A')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_A')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_B:
        """O respondente procurou informações na internet para assistir a shows de música ou apresentações musicais?"""
        _label = 'O respondente procurou informações na internet para assistir a shows de música ou apresentações musicais?'
        NAO = MetaValue(0.0, 'TC13_B')
        SIM = MetaValue(1.0, 'TC13_B')
        NAO_SABE = MetaValue(97.0, 'TC13_B')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_B')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_C:
        """O respondente procurou informações na internet para assistir a peças ou espetáculos no teatro?"""
        _label = 'O respondente procurou informações na internet para assistir a peças ou espetáculos no teatro?'
        NAO = MetaValue(0.0, 'TC13_C')
        SIM = MetaValue(1.0, 'TC13_C')
        NAO_SABE = MetaValue(97.0, 'TC13_C')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_C')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_D:
        """O respondente procurou informações na internet para ir a festas, festivais ou eventos públicos?"""
        _label = 'O respondente procurou informações na internet para ir a festas, festivais ou eventos públicos?'
        NAO = MetaValue(0.0, 'TC13_D')
        SIM = MetaValue(1.0, 'TC13_D')
        NAO_SABE = MetaValue(97.0, 'TC13_D')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_D')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_E:
        """O respondente procurou informações na internet para ir a feiras de arte, artesanato ou antiguidades?"""
        _label = 'O respondente procurou informações na internet para ir a feiras de arte, artesanato ou antiguidades?'
        NAO = MetaValue(0.0, 'TC13_E')
        SIM = MetaValue(1.0, 'TC13_E')
        NAO_SABE = MetaValue(97.0, 'TC13_E')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_E')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_F:
        """O respondente procurou informações na internet para ir a museus ou exposições?"""
        _label = 'O respondente procurou informações na internet para ir a museus ou exposições?'
        NAO = MetaValue(0.0, 'TC13_F')
        SIM = MetaValue(1.0, 'TC13_F')
        NAO_SABE = MetaValue(97.0, 'TC13_F')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_F')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_G:
        """O respondente procurou informações na internet para visitar monumentos ou lugares históricos?"""
        _label = 'O respondente procurou informações na internet para visitar monumentos ou lugares históricos?'
        NAO = MetaValue(0.0, 'TC13_G')
        SIM = MetaValue(1.0, 'TC13_G')
        NAO_SABE = MetaValue(97.0, 'TC13_G')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_G')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class TC13_H:
        """O respondente procurou informações na internet para ir a bibliotecas?"""
        _label = 'O respondente procurou informações na internet para ir a bibliotecas?'
        NAO = MetaValue(0.0, 'TC13_H')
        SIM = MetaValue(1.0, 'TC13_H')
        NAO_SABE = MetaValue(97.0, 'TC13_H')
        NAO_RESPONDEU = MetaValue(98.0, 'TC13_H')
        NAO_SE_APLICA = MetaValue(99.0, 'TC13_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_A:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a documentos pessoais, como RG, CPF, passaporte, ou carteira de trabalho?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a documentos pessoais, como RG, CPF, passaporte, ou carteira de trabalho?'
        NAO = MetaValue(0.0, 'G1_A')
        SIM = MetaValue(1.0, 'G1_A')
        NAO_SABE = MetaValue(97.0, 'G1_A')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_A')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_B:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a saúde pública, como agendamento de consultas, remédios ou outros serviços do sistema público de saúde?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a saúde pública, como agendamento de consultas, remédios ou outros serviços do sistema público de saúde?'
        NAO = MetaValue(0.0, 'G1_B')
        SIM = MetaValue(1.0, 'G1_B')
        NAO_SABE = MetaValue(97.0, 'G1_B')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_B')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_C:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a educação pública, como ENEM, PROUNI, matrícula em escolas ou universidades públicas?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a educação pública, como ENEM, PROUNI, matrícula em escolas ou universidades públicas?'
        NAO = MetaValue(0.0, 'G1_C')
        SIM = MetaValue(1.0, 'G1_C')
        NAO_SABE = MetaValue(97.0, 'G1_C')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_C')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_D:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a direitos do trabalhador ou previdência social, como INSS, FGTS, seguro-desemprego, auxílio-doença, ou aposentadoria?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a direitos do trabalhador ou previdência social, como INSS, FGTS, seguro-desemprego, auxílio-doença, ou aposentadoria?'
        NAO = MetaValue(0.0, 'G1_D')
        SIM = MetaValue(1.0, 'G1_D')
        NAO_SABE = MetaValue(97.0, 'G1_D')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_D')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_E:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a impostos e taxas governamentais, como declaração de imposto de renda, IPVA, ou IPTU?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a impostos e taxas governamentais, como declaração de imposto de renda, IPVA, ou IPTU?'
        NAO = MetaValue(0.0, 'G1_E')
        SIM = MetaValue(1.0, 'G1_E')
        NAO_SABE = MetaValue(97.0, 'G1_E')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_E')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_F:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a polícia e segurança como boletim de ocorrência, antecedentes criminais ou denúncias?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a polícia e segurança como boletim de ocorrência, antecedentes criminais ou denúncias?'
        NAO = MetaValue(0.0, 'G1_F')
        SIM = MetaValue(1.0, 'G1_F')
        NAO_SABE = MetaValue(97.0, 'G1_F')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_F')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_G:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a transporte público ou outros serviços urbanos, como limpeza e conservação de vias, iluminação?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a transporte público ou outros serviços urbanos, como limpeza e conservação de vias, iluminação?'
        NAO = MetaValue(0.0, 'G1_G')
        SIM = MetaValue(1.0, 'G1_G')
        NAO_SABE = MetaValue(97.0, 'G1_G')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_G')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G1_H:
        """Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a Justiça, como consulta de processos ou defensoria pública?"""
        _label = 'Nos últimos 12 meses, o respondente usou a Internet para procurar informações ou realizar serviços públicos relacionados a Justiça, como consulta de processos ou defensoria pública?'
        NAO = MetaValue(0.0, 'G1_H')
        SIM = MetaValue(1.0, 'G1_H')
        NAO_SABE = MetaValue(97.0, 'G1_H')
        NAO_RESPONDEU = MetaValue(98.0, 'G1_H')
        NAO_SE_APLICA = MetaValue(99.0, 'G1_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_A:
        """O respondente realizou serviços referentes a documentos pessoais, como RG, CPF, passaporte, ou carteira de trabalho sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a documentos pessoais, como RG, CPF, passaporte, ou carteira de trabalho sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_A')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_A')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_A')
        NAO_SABE = MetaValue(97.0, 'G2_A')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_A')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_A')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_B:
        """O respondente realizou serviços referentes a saúde pública, como agendamento de consultas, remédios ou outros serviços do sistema público de saúde sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a saúde pública, como agendamento de consultas, remédios ou outros serviços do sistema público de saúde sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_B')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_B')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_B')
        NAO_SABE = MetaValue(97.0, 'G2_B')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_B')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_B')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_C:
        """O respondente realizou serviços referentes a educação pública, como ENEM, PROUNI, matrícula em escolas ou universidades públicas sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a educação pública, como ENEM, PROUNI, matrícula em escolas ou universidades públicas sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_C')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_C')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_C')
        NAO_SABE = MetaValue(97.0, 'G2_C')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_C')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_C')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_D:
        """O respondente realizou serviços referentes a direitos do trabalhador ou previdência social, como INSS, FGTS, seguro-desemprego, auxílio-doença, ou aposentadoria sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a direitos do trabalhador ou previdência social, como INSS, FGTS, seguro-desemprego, auxílio-doença, ou aposentadoria sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_D')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_D')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_D')
        NAO_SABE = MetaValue(97.0, 'G2_D')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_D')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_D')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_E:
        """O respondente realizou serviços referentes a impostos e taxas governamentais, como declaração de imposto de renda, IPVA, ou IPTU sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a impostos e taxas governamentais, como declaração de imposto de renda, IPVA, ou IPTU sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_E')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_E')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_E')
        NAO_SABE = MetaValue(97.0, 'G2_E')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_E')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_E')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_F:
        """O respondente realizou serviços referentes a polícia e segurança como boletim de ocorrência, antecedentes criminais ou denúncias sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a polícia e segurança como boletim de ocorrência, antecedentes criminais ou denúncias sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_F')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_F')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_F')
        NAO_SABE = MetaValue(97.0, 'G2_F')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_F')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_F')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_G:
        """O respondente realizou serviços referentes a transporte público ou outros serviços urbanos, como limpeza e conservação de vias, iluminação sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a transporte público ou outros serviços urbanos, como limpeza e conservação de vias, iluminação sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_G')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_G')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_G')
        NAO_SABE = MetaValue(97.0, 'G2_G')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_G')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_G')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G2_H:
        """O respondente realizou serviços referentes a Justiça, como consulta de processos ou defensoria pública sem precisar se deslocar até um posto de atendimento para finalizá-lo?"""
        _label = 'O respondente realizou serviços referentes a Justiça, como consulta de processos ou defensoria pública sem precisar se deslocar até um posto de atendimento para finalizá-lo?'
        REALIZOU_SERVICO_NA_INTERNET_SEM_PRECISAR_IR_ATE_UM_POSTO = MetaValue(1.0, 'G2_H')
        REALIZOU_PARTE_DO_SERVICO_NA_INTERNET_MAS_PRECISOU_IR_A_UM_POSTO_PARA_FINALIZAR = MetaValue(2.0, 'G2_H')
        APENAS_PROCUROU_INFORMACOES_NA_INTERNET = MetaValue(3.0, 'G2_H')
        NAO_SABE = MetaValue(97.0, 'G2_H')
        NAO_RESPONDEU = MetaValue(98.0, 'G2_H')
        NAO_SE_APLICA = MetaValue(99.0, 'G2_H')
        _map = {1.0: 'Realizou serviço na Internet sem precisar ir até um posto', 2.0: 'Realizou parte do serviço na Internet, mas precisou ir a um posto para finalizar', 3.0: 'Apenas procurou informações na Internet', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G5_A:
        """E nos últimos 12 meses, o(a) sr.(a) acessou o Gov.br para realizar algum serviço público para você mesmo(a)?"""
        _label = 'E nos últimos 12 meses, o(a) sr.(a) acessou o Gov.br para realizar algum serviço público para você mesmo(a)?'
        NAO = MetaValue(0.0, 'G5_A')
        SIM = MetaValue(1.0, 'G5_A')
        NAO_SABE = MetaValue(97.0, 'G5_A')
        NAO_RESPONDEU = MetaValue(98.0, 'G5_A')
        NAO_SE_APLICA = MetaValue(99.0, 'G5_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G5_B:
        """E nos últimos 12 meses, o(a) sr.(a) acessou o Gov.br para realizar algum serviço público para outra pessoa?"""
        _label = 'E nos últimos 12 meses, o(a) sr.(a) acessou o Gov.br para realizar algum serviço público para outra pessoa?'
        NAO = MetaValue(0.0, 'G5_B')
        SIM = MetaValue(1.0, 'G5_B')
        NAO_SABE = MetaValue(97.0, 'G5_B')
        NAO_RESPONDEU = MetaValue(98.0, 'G5_B')
        NAO_SE_APLICA = MetaValue(99.0, 'G5_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G5_C:
        """E nos últimos 12 meses, o(a) sr.(a) pediu a outra pessoa para acessar o Gov.br para realizar algum serviço público para você?"""
        _label = 'E nos últimos 12 meses, o(a) sr.(a) pediu a outra pessoa para acessar o Gov.br para realizar algum serviço público para você?'
        NAO = MetaValue(0.0, 'G5_C')
        SIM = MetaValue(1.0, 'G5_C')
        NAO_SABE = MetaValue(97.0, 'G5_C')
        NAO_RESPONDEU = MetaValue(98.0, 'G5_C')
        NAO_SE_APLICA = MetaValue(99.0, 'G5_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_A:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque não encontrou os serviços que precisou na Internet"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque não encontrou os serviços que precisou na Internet'
        NAO = MetaValue(0.0, 'G3A_A')
        SIM = MetaValue(1.0, 'G3A_A')
        NAO_SABE = MetaValue(97.0, 'G3A_A')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_A')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_C:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses?Porque preferiu fazer o contato pessoalmente"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses?Porque preferiu fazer o contato pessoalmente'
        NAO = MetaValue(0.0, 'G3A_C')
        SIM = MetaValue(1.0, 'G3A_C')
        NAO_SABE = MetaValue(97.0, 'G3A_C')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_C')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_E:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque tem preocupação com proteção e segurança dos dados"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque tem preocupação com proteção e segurança dos dados'
        NAO = MetaValue(0.0, 'G3A_E')
        SIM = MetaValue(1.0, 'G3A_E')
        NAO_SABE = MetaValue(97.0, 'G3A_E')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_E')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_F:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque achou difícil procurar a informação ou realizar o serviço pela Internet"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque achou difícil procurar a informação ou realizar o serviço pela Internet'
        NAO = MetaValue(0.0, 'G3A_F')
        SIM = MetaValue(1.0, 'G3A_F')
        NAO_SABE = MetaValue(97.0, 'G3A_F')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_F')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_G:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque não foi possível finalizar os serviços pela Internet"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Porque não foi possível finalizar os serviços pela Internet'
        NAO = MetaValue(0.0, 'G3A_G')
        SIM = MetaValue(1.0, 'G3A_G')
        NAO_SABE = MetaValue(97.0, 'G3A_G')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_G')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_H:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Por falta de necessidade de buscar informações ou realizar serviços públicos nesse período"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Por falta de necessidade de buscar informações ou realizar serviços públicos nesse período'
        NAO = MetaValue(0.0, 'G3A_H')
        SIM = MetaValue(1.0, 'G3A_H')
        NAO_SABE = MetaValue(97.0, 'G3A_H')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_H')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_H')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G3A_I:
        """Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Outros"""
        _label = 'Por quais dos seguintes motivos o(a) sr(a) não procurou informações ou realizou serviços públicos pela Internet nos últimos 12 meses? Outros'
        NAO = MetaValue(0.0, 'G3A_I')
        SIM = MetaValue(1.0, 'G3A_I')
        NAO_SABE = MetaValue(97.0, 'G3A_I')
        NAO_RESPONDEU = MetaValue(98.0, 'G3A_I')
        NAO_SE_APLICA = MetaValue(99.0, 'G3A_I')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G4A_G:
        """Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pela opção de “fale conosco” de um aplicativo de celular?"""
        _label = 'Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pela opção de “fale conosco” de um aplicativo de celular?'
        NAO = MetaValue(0.0, 'G4A_G')
        SIM = MetaValue(1.0, 'G4A_G')
        NAO_SABE = MetaValue(97.0, 'G4A_G')
        NAO_RESPONDEU = MetaValue(98.0, 'G4A_G')
        NAO_SE_APLICA = MetaValue(99.0, 'G4A_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G4A_A:
        """Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Por e-mail?"""
        _label = 'Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Por e-mail?'
        NAO = MetaValue(0.0, 'G4A_A')
        SIM = MetaValue(1.0, 'G4A_A')
        NAO_SABE = MetaValue(97.0, 'G4A_A')
        NAO_RESPONDEU = MetaValue(98.0, 'G4A_A')
        NAO_SE_APLICA = MetaValue(99.0, 'G4A_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G4A_B:
        """Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pelo site, como por formulário eletrônico, bate-papo ou chat?"""
        _label = 'Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pelo site, como por formulário eletrônico, bate-papo ou chat?'
        NAO = MetaValue(0.0, 'G4A_B')
        SIM = MetaValue(1.0, 'G4A_B')
        NAO_SABE = MetaValue(97.0, 'G4A_B')
        NAO_RESPONDEU = MetaValue(98.0, 'G4A_B')
        NAO_SE_APLICA = MetaValue(99.0, 'G4A_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G4A_C:
        """Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pelos perfis oficiais em redes sociais, como Facebook ou X, antigo Twitter?"""
        _label = 'Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Pelos perfis oficiais em redes sociais, como Facebook ou X, antigo Twitter?'
        NAO = MetaValue(0.0, 'G4A_C')
        SIM = MetaValue(1.0, 'G4A_C')
        NAO_SABE = MetaValue(97.0, 'G4A_C')
        NAO_RESPONDEU = MetaValue(98.0, 'G4A_C')
        NAO_SE_APLICA = MetaValue(99.0, 'G4A_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class G4A_F:
        """Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Por aplicativo de mensagens, como WhatsApp ou Telegram?"""
        _label = 'Nos últimos 12 meses, o(a) sr(a) entrou em contato com o governo ou com instituições públicas Por aplicativo de mensagens, como WhatsApp ou Telegram?'
        NAO = MetaValue(0.0, 'G4A_F')
        SIM = MetaValue(1.0, 'G4A_F')
        NAO_SABE = MetaValue(97.0, 'G4A_F')
        NAO_RESPONDEU = MetaValue(98.0, 'G4A_F')
        NAO_SE_APLICA = MetaValue(99.0, 'G4A_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C1_COB_A:
        """O(A) sr(a) já enviou ou recebeu e-mails?"""
        _label = 'O(A) sr(a) já enviou ou recebeu e-mails?'
        NAO = MetaValue(0.0, 'C1_COB_A')
        SIM = MetaValue(1.0, 'C1_COB_A')
        NAO_SABE = MetaValue(97.0, 'C1_COB_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C1_COB_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C1_COB_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C1_COB_B:
        """O(A) sr(a) Já mandou mensagens por WhatsApp ou Telegram?"""
        _label = 'O(A) sr(a) Já mandou mensagens por WhatsApp ou Telegram?'
        NAO = MetaValue(0.0, 'C1_COB_B')
        SIM = MetaValue(1.0, 'C1_COB_B')
        NAO_SABE = MetaValue(97.0, 'C1_COB_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C1_COB_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C1_COB_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C1_COB_C1:
        """O(A) sr(a) Já usou redes sociais como Facebook ou TikTok?"""
        _label = 'O(A) sr(a) Já usou redes sociais como Facebook ou TikTok?'
        NAO = MetaValue(0.0, 'C1_COB_C1')
        SIM = MetaValue(1.0, 'C1_COB_C1')
        NAO_SABE = MetaValue(97.0, 'C1_COB_C1')
        NAO_RESPONDEU = MetaValue(98.0, 'C1_COB_C1')
        NAO_SE_APLICA = MetaValue(99.0, 'C1_COB_C1')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C1_COB_D:
        """O(A) sr(a) Já buscou informações no Google ou Bing?"""
        _label = 'O(A) sr(a) Já buscou informações no Google ou Bing?'
        NAO = MetaValue(0.0, 'C1_COB_D')
        SIM = MetaValue(1.0, 'C1_COB_D')
        NAO_SABE = MetaValue(97.0, 'C1_COB_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C1_COB_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C1_COB_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C3_COB:
        """Quando o(a) sr(a) fez essas atividaes pela última vez?"""
        _label = 'Quando o(a) sr(a) fez essas atividaes pela última vez?'
        HA_MENOS_DE_3_MESES = MetaValue(1.0, 'C3_COB')
        ENTRE_3_MESES_E_12_MESES = MetaValue(2.0, 'C3_COB')
        MAIS_DE_12_MESES_ATRAS = MetaValue(3.0, 'C3_COB')
        NAO_SABE = MetaValue(97.0, 'C3_COB')
        NAO_RESPONDEU = MetaValue(98.0, 'C3_COB')
        NAO_SE_APLICA = MetaValue(99.0, 'C3_COB')
        _map = {1.0: 'Há menos de 3 meses', 2.0: 'Entre 3 meses e 12 meses', 3.0: 'Mais de 12 meses atrás', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C4_COB:
        """Em média, com que frequência o(a) senhor(a) fez essa(s) atividade(s) nos últimos 3 meses?"""
        _label = 'Em média, com que frequência o(a) senhor(a) fez essa(s) atividade(s) nos últimos 3 meses?'
        TODOS_OS_DIAS_OU_QUASE_TODOS_OS_DIAS = MetaValue(1.0, 'C4_COB')
        PELO_MENOS_UMA_VEZ_POR_SEMANA = MetaValue(2.0, 'C4_COB')
        PELO_MENOS_UMA_VEZ_POR_MES = MetaValue(3.0, 'C4_COB')
        MENOS_DO_QUE_UMA_VEZ_POR_MES = MetaValue(4.0, 'C4_COB')
        NAO_SABE = MetaValue(97.0, 'C4_COB')
        NAO_RESPONDEU = MetaValue(98.0, 'C4_COB')
        NAO_SE_APLICA = MetaValue(99.0, 'C4_COB')
        _map = {1.0: 'Todos os dias ou quase todos os dias', 2.0: 'Pelo menos uma vez por semana', 3.0: 'Pelo menos uma vez por mês', 4.0: 'Menos do que uma vez por mês', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_A:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades no computador de mesa?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades no computador de mesa?'
        NAO = MetaValue(0.0, 'C5_COB_A')
        SIM = MetaValue(1.0, 'C5_COB_A')
        NAO_SABE = MetaValue(97.0, 'C5_COB_A')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_B:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades no notebook?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades no notebook?'
        NAO = MetaValue(0.0, 'C5_COB_B')
        SIM = MetaValue(1.0, 'C5_COB_B')
        NAO_SABE = MetaValue(97.0, 'C5_COB_B')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_B')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_B')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_C:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades no tablet?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades no tablet?'
        NAO = MetaValue(0.0, 'C5_COB_C')
        SIM = MetaValue(1.0, 'C5_COB_C')
        NAO_SABE = MetaValue(97.0, 'C5_COB_C')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_D:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades no telefone celular?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades no telefone celular?'
        NAO = MetaValue(0.0, 'C5_COB_D')
        SIM = MetaValue(1.0, 'C5_COB_D')
        NAO_SABE = MetaValue(97.0, 'C5_COB_D')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_E:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades no videogame?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades no videogame?'
        NAO = MetaValue(0.0, 'C5_COB_E')
        SIM = MetaValue(1.0, 'C5_COB_E')
        NAO_SABE = MetaValue(97.0, 'C5_COB_E')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_F:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades na televisão?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades na televisão?'
        NAO = MetaValue(0.0, 'C5_COB_F')
        SIM = MetaValue(1.0, 'C5_COB_F')
        NAO_SABE = MetaValue(97.0, 'C5_COB_F')
        NAO_RESPONDEU = MetaValue(98.0, 'C5_COB_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class C5_COB_G:
        """Nos últimos 3 meses o(a) sr(a) fez essas atividades em outro aparelho?"""
        _label = 'Nos últimos 3 meses o(a) sr(a) fez essas atividades em outro aparelho?'
        NAO = MetaValue(0.0, 'C5_COB_G')
        SIM = MetaValue(1.0, 'C5_COB_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C5_COB_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_A:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades em casa?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades em casa?'
        NAO = MetaValue(0.0, 'C6_COB_A')
        SIM = MetaValue(1.0, 'C6_COB_A')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_A')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_B1:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades no local de trabalho, sem contar sua própria casa?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades no local de trabalho, sem contar sua própria casa?'
        NAO = MetaValue(0.0, 'C6_COB_B1')
        SIM = MetaValue(1.0, 'C6_COB_B1')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_B1')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_C:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades na escola ou estabelecimento de ensino?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades na escola ou estabelecimento de ensino?'
        NAO = MetaValue(0.0, 'C6_COB_C')
        SIM = MetaValue(1.0, 'C6_COB_C')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_C')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_D:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades na casa de outra pessoa, como por exemplo amigo, vizinho ou familiar?'
        NAO = MetaValue(0.0, 'C6_COB_D')
        SIM = MetaValue(1.0, 'C6_COB_D')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_D')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_E:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades no centro público de acesso gratuito, como por exemplo telecentro, biblioteca ou entidade comunitária?'
        NAO = MetaValue(0.0, 'C6_COB_E')
        SIM = MetaValue(1.0, 'C6_COB_E')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_E')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_F:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou Internet café?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades no centro público de acesso pago, como por exemplo lanhouse, Cyber Café ou Internet café?'
        NAO = MetaValue(0.0, 'C6_COB_F')
        SIM = MetaValue(1.0, 'C6_COB_F')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_F')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_G:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades enquanto se desloca, como por exemplo na rua, no ônibus, no metrô ou no carro?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades enquanto se desloca, como por exemplo na rua, no ônibus, no metrô ou no carro?'
        NAO = MetaValue(0.0, 'C6_COB_G')
        SIM = MetaValue(1.0, 'C6_COB_G')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_G')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class C6_COB_OUTRO:
        """Pensando nos últimos 3 meses, o respondente fez essas atividades em outro lugar?"""
        _label = 'Pensando nos últimos 3 meses, o respondente fez essas atividades em outro lugar?'
        NAO = MetaValue(0.0, 'C6_COB_OUTRO')
        SIM = MetaValue(1.0, 'C6_COB_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'C6_COB_OUTRO')
        _map = {0.0: 'Não', 1.0: 'Sim', 99.0: 'Não se aplica'}

    class PESO:
        """None"""
        _label = None
        pass

    class rep1:
        """None"""
        _label = None
        pass

    class rep2:
        """None"""
        _label = None
        pass

    class rep3:
        """None"""
        _label = None
        pass

    class rep4:
        """None"""
        _label = None
        pass

    class rep5:
        """None"""
        _label = None
        pass

    class rep6:
        """None"""
        _label = None
        pass

    class rep7:
        """None"""
        _label = None
        pass

    class rep8:
        """None"""
        _label = None
        pass

    class rep9:
        """None"""
        _label = None
        pass

    class rep10:
        """None"""
        _label = None
        pass

    class rep11:
        """None"""
        _label = None
        pass

    class rep12:
        """None"""
        _label = None
        pass

    class rep13:
        """None"""
        _label = None
        pass

    class rep14:
        """None"""
        _label = None
        pass

    class rep15:
        """None"""
        _label = None
        pass

    class rep16:
        """None"""
        _label = None
        pass

    class rep17:
        """None"""
        _label = None
        pass

    class rep18:
        """None"""
        _label = None
        pass

    class rep19:
        """None"""
        _label = None
        pass

    class rep20:
        """None"""
        _label = None
        pass

    class rep21:
        """None"""
        _label = None
        pass

    class rep22:
        """None"""
        _label = None
        pass

    class rep23:
        """None"""
        _label = None
        pass

    class rep24:
        """None"""
        _label = None
        pass

    class rep25:
        """None"""
        _label = None
        pass

    class rep26:
        """None"""
        _label = None
        pass

    class rep27:
        """None"""
        _label = None
        pass

    class rep28:
        """None"""
        _label = None
        pass

    class rep29:
        """None"""
        _label = None
        pass

    class rep30:
        """None"""
        _label = None
        pass

    class rep31:
        """None"""
        _label = None
        pass

    class rep32:
        """None"""
        _label = None
        pass

    class rep33:
        """None"""
        _label = None
        pass

    class rep34:
        """None"""
        _label = None
        pass

    class rep35:
        """None"""
        _label = None
        pass

    class rep36:
        """None"""
        _label = None
        pass

    class rep37:
        """None"""
        _label = None
        pass

    class rep38:
        """None"""
        _label = None
        pass

    class rep39:
        """None"""
        _label = None
        pass

    class rep40:
        """None"""
        _label = None
        pass

    class rep41:
        """None"""
        _label = None
        pass

    class rep42:
        """None"""
        _label = None
        pass

    class rep43:
        """None"""
        _label = None
        pass

    class rep44:
        """None"""
        _label = None
        pass

    class rep45:
        """None"""
        _label = None
        pass

    class rep46:
        """None"""
        _label = None
        pass

    class rep47:
        """None"""
        _label = None
        pass

    class rep48:
        """None"""
        _label = None
        pass

    class rep49:
        """None"""
        _label = None
        pass

    class rep50:
        """None"""
        _label = None
        pass

    class rep51:
        """None"""
        _label = None
        pass

    class rep52:
        """None"""
        _label = None
        pass

    class rep53:
        """None"""
        _label = None
        pass

    class rep54:
        """None"""
        _label = None
        pass

    class rep55:
        """None"""
        _label = None
        pass

    class rep56:
        """None"""
        _label = None
        pass

    class rep57:
        """None"""
        _label = None
        pass

    class rep58:
        """None"""
        _label = None
        pass

    class rep59:
        """None"""
        _label = None
        pass

    class rep60:
        """None"""
        _label = None
        pass

    class rep61:
        """None"""
        _label = None
        pass

    class rep62:
        """None"""
        _label = None
        pass

    class rep63:
        """None"""
        _label = None
        pass

    class rep64:
        """None"""
        _label = None
        pass

    class rep65:
        """None"""
        _label = None
        pass

    class rep66:
        """None"""
        _label = None
        pass

    class rep67:
        """None"""
        _label = None
        pass

    class rep68:
        """None"""
        _label = None
        pass

    class rep69:
        """None"""
        _label = None
        pass

    class rep70:
        """None"""
        _label = None
        pass

    class rep71:
        """None"""
        _label = None
        pass

    class rep72:
        """None"""
        _label = None
        pass

    class rep73:
        """None"""
        _label = None
        pass

    class rep74:
        """None"""
        _label = None
        pass

    class rep75:
        """None"""
        _label = None
        pass

    class rep76:
        """None"""
        _label = None
        pass

    class rep77:
        """None"""
        _label = None
        pass

    class rep78:
        """None"""
        _label = None
        pass

    class rep79:
        """None"""
        _label = None
        pass

    class rep80:
        """None"""
        _label = None
        pass

    class rep81:
        """None"""
        _label = None
        pass

    class rep82:
        """None"""
        _label = None
        pass

    class rep83:
        """None"""
        _label = None
        pass

    class rep84:
        """None"""
        _label = None
        pass

    class rep85:
        """None"""
        _label = None
        pass

    class rep86:
        """None"""
        _label = None
        pass

    class rep87:
        """None"""
        _label = None
        pass

    class rep88:
        """None"""
        _label = None
        pass

    class rep89:
        """None"""
        _label = None
        pass

    class rep90:
        """None"""
        _label = None
        pass

    class rep91:
        """None"""
        _label = None
        pass

    class rep92:
        """None"""
        _label = None
        pass

    class rep93:
        """None"""
        _label = None
        pass

    class rep94:
        """None"""
        _label = None
        pass

    class rep95:
        """None"""
        _label = None
        pass

    class rep96:
        """None"""
        _label = None
        pass

    class rep97:
        """None"""
        _label = None
        pass

    class rep98:
        """None"""
        _label = None
        pass

    class rep99:
        """None"""
        _label = None
        pass

    class rep100:
        """None"""
        _label = None
        pass

    class rep101:
        """None"""
        _label = None
        pass

    class rep102:
        """None"""
        _label = None
        pass

    class rep103:
        """None"""
        _label = None
        pass

    class rep104:
        """None"""
        _label = None
        pass

    class rep105:
        """None"""
        _label = None
        pass

    class rep106:
        """None"""
        _label = None
        pass

    class rep107:
        """None"""
        _label = None
        pass

    class rep108:
        """None"""
        _label = None
        pass

    class rep109:
        """None"""
        _label = None
        pass

    class rep110:
        """None"""
        _label = None
        pass

    class rep111:
        """None"""
        _label = None
        pass

    class rep112:
        """None"""
        _label = None
        pass

    class rep113:
        """None"""
        _label = None
        pass

    class rep114:
        """None"""
        _label = None
        pass

    class rep115:
        """None"""
        _label = None
        pass

    class rep116:
        """None"""
        _label = None
        pass

    class rep117:
        """None"""
        _label = None
        pass

    class rep118:
        """None"""
        _label = None
        pass

    class rep119:
        """None"""
        _label = None
        pass

    class rep120:
        """None"""
        _label = None
        pass

    class rep121:
        """None"""
        _label = None
        pass

    class rep122:
        """None"""
        _label = None
        pass

    class rep123:
        """None"""
        _label = None
        pass

    class rep124:
        """None"""
        _label = None
        pass

    class rep125:
        """None"""
        _label = None
        pass

    class rep126:
        """None"""
        _label = None
        pass

    class rep127:
        """None"""
        _label = None
        pass

    class rep128:
        """None"""
        _label = None
        pass

    class rep129:
        """None"""
        _label = None
        pass

    class rep130:
        """None"""
        _label = None
        pass

    class rep131:
        """None"""
        _label = None
        pass

    class rep132:
        """None"""
        _label = None
        pass

    class rep133:
        """None"""
        _label = None
        pass

    class rep134:
        """None"""
        _label = None
        pass

    class rep135:
        """None"""
        _label = None
        pass

    class rep136:
        """None"""
        _label = None
        pass

    class rep137:
        """None"""
        _label = None
        pass

    class rep138:
        """None"""
        _label = None
        pass

    class rep139:
        """None"""
        _label = None
        pass

    class rep140:
        """None"""
        _label = None
        pass

    class rep141:
        """None"""
        _label = None
        pass

    class rep142:
        """None"""
        _label = None
        pass

    class rep143:
        """None"""
        _label = None
        pass

    class rep144:
        """None"""
        _label = None
        pass

    class rep145:
        """None"""
        _label = None
        pass

    class rep146:
        """None"""
        _label = None
        pass

    class rep147:
        """None"""
        _label = None
        pass

    class rep148:
        """None"""
        _label = None
        pass

    class rep149:
        """None"""
        _label = None
        pass

    class rep150:
        """None"""
        _label = None
        pass

    class rep151:
        """None"""
        _label = None
        pass

    class rep152:
        """None"""
        _label = None
        pass

    class rep153:
        """None"""
        _label = None
        pass

    class rep154:
        """None"""
        _label = None
        pass

    class rep155:
        """None"""
        _label = None
        pass

    class rep156:
        """None"""
        _label = None
        pass

    class rep157:
        """None"""
        _label = None
        pass

    class rep158:
        """None"""
        _label = None
        pass

    class rep159:
        """None"""
        _label = None
        pass

    class rep160:
        """None"""
        _label = None
        pass

    class rep161:
        """None"""
        _label = None
        pass

    class rep162:
        """None"""
        _label = None
        pass

    class rep163:
        """None"""
        _label = None
        pass

    class rep164:
        """None"""
        _label = None
        pass

    class rep165:
        """None"""
        _label = None
        pass

    class rep166:
        """None"""
        _label = None
        pass

    class rep167:
        """None"""
        _label = None
        pass

    class rep168:
        """None"""
        _label = None
        pass

    class rep169:
        """None"""
        _label = None
        pass

    class rep170:
        """None"""
        _label = None
        pass

    class rep171:
        """None"""
        _label = None
        pass

    class rep172:
        """None"""
        _label = None
        pass

    class rep173:
        """None"""
        _label = None
        pass

    class rep174:
        """None"""
        _label = None
        pass

    class rep175:
        """None"""
        _label = None
        pass

    class rep176:
        """None"""
        _label = None
        pass

    class rep177:
        """None"""
        _label = None
        pass

    class rep178:
        """None"""
        _label = None
        pass

    class rep179:
        """None"""
        _label = None
        pass

    class rep180:
        """None"""
        _label = None
        pass

    class rep181:
        """None"""
        _label = None
        pass

    class rep182:
        """None"""
        _label = None
        pass

    class rep183:
        """None"""
        _label = None
        pass

    class rep184:
        """None"""
        _label = None
        pass

    class rep185:
        """None"""
        _label = None
        pass

    class rep186:
        """None"""
        _label = None
        pass

    class rep187:
        """None"""
        _label = None
        pass

    class rep188:
        """None"""
        _label = None
        pass

    class rep189:
        """None"""
        _label = None
        pass

    class rep190:
        """None"""
        _label = None
        pass

    class rep191:
        """None"""
        _label = None
        pass

    class rep192:
        """None"""
        _label = None
        pass

    class rep193:
        """None"""
        _label = None
        pass

    class rep194:
        """None"""
        _label = None
        pass

    class rep195:
        """None"""
        _label = None
        pass

    class rep196:
        """None"""
        _label = None
        pass

    class rep197:
        """None"""
        _label = None
        pass

    class rep198:
        """None"""
        _label = None
        pass

    class rep199:
        """None"""
        _label = None
        pass

    class rep200:
        """None"""
        _label = None
        pass

    class AREA:
        """Área"""
        _label = 'Área'
        URBANA = MetaValue(1.0, 'AREA')
        RURAL = MetaValue(2.0, 'AREA')
        _map = {1.0: 'URBANA', 2.0: 'RURAL'}

    class COD_UF:
        """UF (listagem  com código do IBGE)"""
        _label = 'UF (listagem  com código do IBGE)'
        RONDONIA = MetaValue(11.0, 'COD_UF')
        ACRE = MetaValue(12.0, 'COD_UF')
        AMAZONAS = MetaValue(13.0, 'COD_UF')
        RORAIMA = MetaValue(14.0, 'COD_UF')
        PARA = MetaValue(15.0, 'COD_UF')
        AMAPA = MetaValue(16.0, 'COD_UF')
        TOCANTINS = MetaValue(17.0, 'COD_UF')
        MARANHAO = MetaValue(21.0, 'COD_UF')
        PIAUI = MetaValue(22.0, 'COD_UF')
        CEARA = MetaValue(23.0, 'COD_UF')
        RIO_GRANDE_DO_NORTE = MetaValue(24.0, 'COD_UF')
        PARAIBA = MetaValue(25.0, 'COD_UF')
        PERNAMBUCO = MetaValue(26.0, 'COD_UF')
        ALAGOAS = MetaValue(27.0, 'COD_UF')
        SERGIPE = MetaValue(28.0, 'COD_UF')
        BAHIA = MetaValue(29.0, 'COD_UF')
        MINAS_GERAIS = MetaValue(31.0, 'COD_UF')
        ESPIRITO_SANTO = MetaValue(32.0, 'COD_UF')
        RIO_DE_JANEIRO = MetaValue(33.0, 'COD_UF')
        SAO_PAULO = MetaValue(35.0, 'COD_UF')
        PARANA = MetaValue(41.0, 'COD_UF')
        SANTA_CATARINA = MetaValue(42.0, 'COD_UF')
        RIO_GRANDE_DO_SUL = MetaValue(43.0, 'COD_UF')
        MATO_GROSSO_DO_SUL = MetaValue(50.0, 'COD_UF')
        MATO_GROSSO = MetaValue(51.0, 'COD_UF')
        GOIAS = MetaValue(52.0, 'COD_UF')
        DISTRITO_FEDERAL = MetaValue(53.0, 'COD_UF')
        _map = {11.0: 'RONDÔNIA', 12.0: 'ACRE', 13.0: 'AMAZONAS', 14.0: 'RORAIMA', 15.0: 'PARÁ', 16.0: 'AMAPÁ', 17.0: 'TOCANTINS', 21.0: 'MARANHÃO', 22.0: 'PIAUÍ', 23.0: 'CEARÁ', 24.0: 'RIO GRANDE DO NORTE', 25.0: 'PARAÍBA', 26.0: 'PERNAMBUCO', 27.0: 'ALAGOAS', 28.0: 'SERGIPE', 29.0: 'BAHIA', 31.0: 'MINAS GERAIS', 32.0: 'ESPIRITO SANTO', 33.0: 'RIO DE JANEIRO', 35.0: 'SÃO PAULO', 41.0: 'PARANÁ', 42.0: 'SANTA CATARINA', 43.0: 'RIO GRANDE DO SUL', 50.0: 'MATO GROSSO DO SUL', 51.0: 'MATO GROSSO', 52.0: 'GOIÁS', 53.0: 'DISTRITO FEDERAL'}

    class RENDA_FAMILIAR:
        """Renda familiar"""
        _label = 'Renda familiar'
        ATE_R_151800 = MetaValue(1.0, 'RENDA_FAMILIAR')
        DE_R_151801_ATE_R_303600 = MetaValue(2.0, 'RENDA_FAMILIAR')
        DE_R_303601_ATE_R_455400 = MetaValue(3.0, 'RENDA_FAMILIAR')
        DE_R_455401_ATE_R_759000 = MetaValue(4.0, 'RENDA_FAMILIAR')
        DE_R_759001_ATE_R_1518000 = MetaValue(5.0, 'RENDA_FAMILIAR')
        DE_R_1518001_ATE_R_3036000 = MetaValue(6.0, 'RENDA_FAMILIAR')
        DE_R_3036001_ATE_R_4554000 = MetaValue(7.0, 'RENDA_FAMILIAR')
        MAIS_DE_R_4554000 = MetaValue(8.0, 'RENDA_FAMILIAR')
        NAO_TEM_RENDA = MetaValue(9.0, 'RENDA_FAMILIAR')
        NAO_SABE = MetaValue(97.0, 'RENDA_FAMILIAR')
        NAO_RESPONDEU = MetaValue(98.0, 'RENDA_FAMILIAR')
        _map = {1.0: 'Até R$ 1.518,00', 2.0: 'De R$ 1.518,01 até R$ 3.036,00', 3.0: 'De R$ 3.036,01 até R$ 4.554,00', 4.0: 'De R$ 4.554,01 até R$ 7.590,00', 5.0: 'De R$ 7.590,01 até R$ 15.180,00', 6.0: 'De R$ 15.180,01 até R$ 30.360,00', 7.0: 'De R$ 30.360,01 até R$ 45.540,00', 8.0: 'Mais de R$ 45.540,00', 9.0: 'Não tem renda', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class COD_REGIAO_2:
        """Região"""
        _label = 'Região'
        SUDESTE = MetaValue(1.0, 'COD_REGIAO_2')
        NORDESTE = MetaValue(2.0, 'COD_REGIAO_2')
        SUL = MetaValue(3.0, 'COD_REGIAO_2')
        NORTE = MetaValue(4.0, 'COD_REGIAO_2')
        CENTRO_OESTE = MetaValue(5.0, 'COD_REGIAO_2')
        _map = {1.0: 'Sudeste', 2.0: 'Nordeste', 3.0: 'Sul', 4.0: 'Norte', 5.0: 'Centro-Oeste'}

    class GRAU_INST_1:
        """Grau de instrução"""
        _label = 'Grau de instrução'
        ANALFABETO_EDUCACAO_INFANTIL = MetaValue(1.0, 'GRAU_INST_1')
        FUNDAMENTAL = MetaValue(2.0, 'GRAU_INST_1')
        MEDIO = MetaValue(3.0, 'GRAU_INST_1')
        SUPERIOR = MetaValue(4.0, 'GRAU_INST_1')
        _map = {1.0: 'Analfabeto/Educação Infantil', 2.0: 'Fundamental', 3.0: 'Médio', 4.0: 'Superior'}

    class RENDA_FAMILIAR_2:
        """Renda familiar"""
        _label = 'Renda familiar'
        ATE_1_SM = MetaValue(1.0, 'RENDA_FAMILIAR_2')
        MAIS_DE_1_SM_ATE_2_SM = MetaValue(2.0, 'RENDA_FAMILIAR_2')
        MAIS_DE_2_SM_ATE_3_SM = MetaValue(3.0, 'RENDA_FAMILIAR_2')
        MAIS_DE_3_SM_ATE_5_SM = MetaValue(4.0, 'RENDA_FAMILIAR_2')
        MAIS_DE_5_SM_ATE_10_SM = MetaValue(5.0, 'RENDA_FAMILIAR_2')
        MAIS_DE_10_SM = MetaValue(6.0, 'RENDA_FAMILIAR_2')
        NAO_TEM_RENDA = MetaValue(7.0, 'RENDA_FAMILIAR_2')
        NAO_SABE = MetaValue(97.0, 'RENDA_FAMILIAR_2')
        NAO_RESPONDEU = MetaValue(98.0, 'RENDA_FAMILIAR_2')
        _map = {1.0: 'Até 1 SM', 2.0: 'Mais de 1 SM até 2 SM', 3.0: 'Mais de 2 SM até 3 SM', 4.0: 'Mais de 3 SM até 5 SM', 5.0: 'Mais de 5 SM até 10 SM', 6.0: 'Mais de 10 SM', 7.0: 'Não tem renda', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class CLASSE_2015:
        """Classe social"""
        _label = 'Classe social'
        A = MetaValue(1.0, 'CLASSE_2015')
        B = MetaValue(2.0, 'CLASSE_2015')
        C = MetaValue(3.0, 'CLASSE_2015')
        DE = MetaValue(4.0, 'CLASSE_2015')
        _map = {1.0: 'A', 2.0: 'B', 3.0: 'C', 4.0: 'DE'}

    class PEA_2:
        """Condição de atividade"""
        _label = 'Condição de atividade'
        NA_FORCA_DE_TRABALHO = MetaValue(1.0, 'PEA_2')
        FORA_DA_FORCA_DE_TRABALHO = MetaValue(2.0, 'PEA_2')
        _map = {1.0: 'Na força de trabalho', 2.0: 'Fora da força de trabalho'}

    class TIPO_OCUP:
        """Tipo de ocupação"""
        _label = 'Tipo de ocupação'
        FORMAL = MetaValue(1.0, 'TIPO_OCUP')
        INFORMAL = MetaValue(2.0, 'TIPO_OCUP')
        INDETERMINADO = MetaValue(3.0, 'TIPO_OCUP')
        NAO_SE_APLICA = MetaValue(99.0, 'TIPO_OCUP')
        _map = {1.0: 'Formal', 2.0: 'Informal', 3.0: 'Indeterminado', 99.0: 'Não se aplica'}

    class F_C3_IDADE:
        """Usuários de Internet com 16 anos ou mais"""
        _label = 'Usuários de Internet com 16 anos ou mais'
        USUARIOS_DE_INTERNET_COM_16_ANOS_OU_MAIS = MetaValue(1.0, 'F_C3_IDADE')
        _map = {1.0: 'Usuários de Internet com 16 anos ou mais'}

    class F_C3_G1_AGREG:
        """Usuários de Internet com 16 anos ou mais que não usaram serviços de governo eletrônico nos últimos doze meses"""
        _label = 'Usuários de Internet com 16 anos ou mais que não usaram serviços de governo eletrônico nos últimos doze meses'
        USUARIOS_DE_INTERNET_COM_16_ANOS_OU_MAIS_QUE_NAO_USARAM_SERVICOS_DE_GOVERNO_ELETRONICO_NOS_ULTIMOS_DOZE_MESES = MetaValue(1.0, 'F_C3_G1_AGREG')
        _map = {1.0: 'Usuários de Internet com 16 anos ou mais que não usaram serviços de governo eletrônico nos últimos doze meses'}

    class F_J5:
        """Pessoas que possuem telefone celular"""
        _label = 'Pessoas que possuem telefone celular'
        PESSOAS_QUE_POSSUEM_TELEFONE_CELULAR = MetaValue(1.0, 'F_J5')
        _map = {1.0: 'Pessoas que possuem telefone celular'}

    class C1_COB_AGREG:
        """Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses"""
        _label = 'Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses'
        SIM = MetaValue(1.0, 'C1_COB_AGREG')
        NAO = MetaValue(0.0, 'C1_COB_AGREG')
        _map = {1.0: 'Sim', 0.0: 'Não'}

    class C3J3:
        """Usuários de internet - indicador ampliado¹"""
        _label = 'Usuários de internet - indicador ampliado¹'
        SIM = MetaValue(1.0, 'C3J3')
        NAO = MetaValue(0.0, 'C3J3')
        NAO_SABE = MetaValue(97.0, 'C3J3')
        NAO_RESPONDEU = MetaValue(98.0, 'C3J3')
        _map = {1.0: 'Sim', 0.0: 'Não', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class C14_AGREG:
        """USUÁRIOS DE INTERNET, POR ATIVIDADES REALIZADAS NA INTERNET - APOSTAS"""
        _label = 'USUÁRIOS DE INTERNET, POR ATIVIDADES REALIZADAS NA INTERNET - APOSTAS'
        FEZ_ALGUM_TIPO_DE_APOSTA = MetaValue(1.0, 'C14_AGREG')
        _map = {1.0: 'Fez algum tipo de aposta'}

    class C5_AGREG:
        """Usuários de internet, por dispositivo utilizado"""
        _label = 'Usuários de internet, por dispositivo utilizado'
        TOTAL___COMPUTADOR = MetaValue(1.0, 'C5_AGREG')
        _map = {1.0: 'Total - Computador'}

    class C5_DISPOSITIVOS:
        """Usuários de internet, por dispositivo utilizado de forma exclusiva ou simultânea para acessar a internet - telefone celular e computador"""
        _label = 'Usuários de internet, por dispositivo utilizado de forma exclusiva ou simultânea para acessar a internet - telefone celular e computador'
        APENAS_COMPUTADOR = MetaValue(1.0, 'C5_DISPOSITIVOS')
        APENAS_TELEFONE_CELULAR = MetaValue(2.0, 'C5_DISPOSITIVOS')
        AMBOS = MetaValue(3.0, 'C5_DISPOSITIVOS')
        NENHUM_DESSES_DISPOSITIVOS = MetaValue(4.0, 'C5_DISPOSITIVOS')
        _map = {1.0: 'Apenas computador', 2.0: 'Apenas telefone celular', 3.0: 'Ambos', 4.0: 'Nenhum desses dispositivos'}

    class C5_DISPOSITIVOS_B:
        """Usuários de internet, por dispositivo utilizado de forma exclusiva ou simultânea para acessar a internet - dispositivos selecionados"""
        _label = 'Usuários de internet, por dispositivo utilizado de forma exclusiva ou simultânea para acessar a internet - dispositivos selecionados'
        APENAS_TELEFONE_CELULAR = MetaValue(1.0, 'C5_DISPOSITIVOS_B')
        TELEFONE_CELULAR_E_TELEVISAO = MetaValue(2.0, 'C5_DISPOSITIVOS_B')
        TELEFONE_CELULAR_TELEVISAO_E_COMPUTADOR = MetaValue(4.0, 'C5_DISPOSITIVOS_B')
        TELEFONE_CELULAR_E_COMPUTADOR = MetaValue(3.0, 'C5_DISPOSITIVOS_B')
        DEMAIS_COMBINACOES = MetaValue(8.0, 'C5_DISPOSITIVOS_B')
        _map = {1.0: 'Apenas telefone celular', 2.0: 'Telefone celular e televisão', 4.0: 'Telefone celular, televisão e computador', 3.0: 'Telefone celular e computador', 8.0: 'Demais combinações'}

    class G1_AGREG:
        """Utilizaram governo eletrônico nos últimos 12 meses"""
        _label = 'Utilizaram governo eletrônico nos últimos 12 meses'
        SIM = MetaValue(1.0, 'G1_AGREG')
        NAO = MetaValue(0.0, 'G1_AGREG')
        _map = {1.0: 'Sim', 0.0: 'Não'}

    class C8_NAO:
        """Não utilizaram a Internet para realizar atividades de interação com autoridades públicas"""
        _label = 'Não utilizaram a Internet para realizar atividades de interação com autoridades públicas'
        NAO_UTILIZOU_A_INTERNET_PARA_REALIZAR_ATIVIDADES_DE_INTERACAO_COM_AUTORIDADES_PUBLICAS = MetaValue(1.0, 'C8_NAO')
        _map = {1.0: 'Não utilizou a Internet para realizar atividades de interação com autoridades públicas'}

    class G5_AGREG:
        """None"""
        _label = None
        pass

    class I1A_NENHUM:
        """Usuários de internet, por tipo de habilidade digital"""
        _label = 'Usuários de internet, por tipo de habilidade digital'
        NENHUMA_DAS_OPCOES = MetaValue(1.0, 'I1A_NENHUM')
        _map = {1.0: 'Nenhuma das opções'}

    class J5_FAIXAS:
        """Quantidade de linhas de telefone celular"""
        _label = 'Quantidade de linhas de telefone celular'
        NENHUMA = MetaValue(0.0, 'J5_FAIXAS')
        UMA = MetaValue(1.0, 'J5_FAIXAS')
        DUAS = MetaValue(2.0, 'J5_FAIXAS')
        TRES_OU_MAIS = MetaValue(3.0, 'J5_FAIXAS')
        NAO_SABE = MetaValue(97.0, 'J5_FAIXAS')
        NAO_RESPONDEU = MetaValue(98.0, 'J5_FAIXAS')
        NAO_SE_APLICA = MetaValue(99.0, 'J5_FAIXAS')
        _map = {0.0: 'Nenhuma', 1.0: 'Uma', 2.0: 'Duas', 3.0: 'Três ou mais', 97.0: 'Não sabe', 98.0: 'Não respondeu', 99.0: 'Não se aplica'}

    class J2_NENHUM:
        """Usuários de telefone celular, por atividades realizadas no telefone celular nos últimos três meses"""
        _label = 'Usuários de telefone celular, por atividades realizadas no telefone celular nos últimos três meses'
        NENHUMA_DESSAS_ATIVIDADES = MetaValue(1.0, 'J2_NENHUM')
        _map = {1.0: 'Nenhuma dessas atividades'}

    class J3_AGREG:
        """Indivíduos que usaram a internet no telefone celular nos últimos três meses¹"""
        _label = 'Indivíduos que usaram a internet no telefone celular nos últimos três meses¹'
        SIM = MetaValue(1.0, 'J3_AGREG')
        NAO = MetaValue(0.0, 'J3_AGREG')
        NAO_SABE = MetaValue(97.0, 'J3_AGREG')
        NAO_RESPONDEU = MetaValue(98.0, 'J3_AGREG')
        _map = {1.0: 'Sim', 0.0: 'Não', 97.0: 'Não sabe', 98.0: 'Não respondeu'}

    class J3AB:
        """Usuários de internet pelo telefone celular, por tipo de conexão utilizada de forma exclusiva ou simultânea"""
        _label = 'Usuários de internet pelo telefone celular, por tipo de conexão utilizada de forma exclusiva ou simultânea'
        APENAS_3G_OU_4G = MetaValue(1.0, 'J3AB')
        APENAS_WI_FI = MetaValue(2.0, 'J3AB')
        AMBOS = MetaValue(3.0, 'J3AB')
        INDETERMINADO1 = MetaValue(4.0, 'J3AB')
        _map = {1.0: 'Apenas 3G ou 4G', 2.0: 'Apenas Wi-Fi', 3.0: 'Ambos', 4.0: 'Indeterminado¹'}

    class C5_COB_AGREG:
        """Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por dispositivo utilizado"""
        _label = 'Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por dispositivo utilizado'
        TOTAL___COMPUTADOR = MetaValue(1.0, 'C5_COB_AGREG')
        _map = {1.0: 'Total - Computador'}

    class C5_COB_NENHUM:
        """Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por dispositivo utilizado"""
        _label = 'Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por dispositivo utilizado'
        NENHUM_DESSES_DISPOSITIVOS = MetaValue(1.0, 'C5_COB_NENHUM')
        _map = {1.0: 'Nenhum desses dispositivos'}

    class C6_COB_NENHUM:
        """Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por local de acesso individual"""
        _label = 'Não usuários de internet que utilizaram alguma aplicação selecionada nos últimos três meses¹, por local de acesso individual'
        EM_NENHUM_DESSES_LUGARES = MetaValue(1.0, 'C6_COB_NENHUM')
        _map = {1.0: 'Em nenhum desses lugares'}

    class TIPO_RM_NUM:
        """None"""
        _label = None
        pass

