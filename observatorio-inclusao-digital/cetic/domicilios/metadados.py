# -*- coding: utf-8 -*-
"""
METADADOS GERADOS AUTOMATICAMENTE
"""

class MetaValue(float):
    def __new__(cls, value, column):
        res = super(MetaValue, cls).__new__(cls, value)
        res.column = column
        return res

class Metadados:
    class QUEST:
        """Número de identificação do questionário"""
        _label = 'Número de identificação do questionário'
        pass

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
        _map = {
            11.0: 'RONDÔNIA',
            12.0: 'ACRE',
            13.0: 'AMAZONAS',
            14.0: 'RORAIMA',
            15.0: 'PARÁ',
            16.0: 'AMAPÁ',
            17.0: 'TOCANTINS',
            21.0: 'MARANHÃO',
            22.0: 'PIAUÍ',
            23.0: 'CEARÁ',
            24.0: 'RIO GRANDE DO NORTE',
            25.0: 'PARAÍBA',
            26.0: 'PERNAMBUCO',
            27.0: 'ALAGOAS',
            28.0: 'SERGIPE',
            29.0: 'BAHIA',
            31.0: 'MINAS GERAIS',
            32.0: 'ESPIRITO SANTO',
            33.0: 'RIO DE JANEIRO',
            35.0: 'SÃO PAULO',
            41.0: 'PARANÁ',
            42.0: 'SANTA CATARINA',
            43.0: 'RIO GRANDE DO SUL',
            50.0: 'MATO GROSSO DO SUL',
            51.0: 'MATO GROSSO',
            52.0: 'GOIÁS',
            53.0: 'DISTRITO FEDERAL',
        }

    class AREA:
        """Área"""
        _label = 'Área'
        URBANA = MetaValue(1.0, 'AREA')
        RURAL = MetaValue(2.0, 'AREA')
        _map = {
            1.0: 'URBANA',
            2.0: 'RURAL',
        }

    class RENDA_FAMILIAR:
        """Renda familiar"""
        _label = 'Renda familiar'
        ATE_1_SM = MetaValue(1.0, 'RENDA_FAMILIAR')
        MAIS_DE_1_SM_ATE_2_SM = MetaValue(2.0, 'RENDA_FAMILIAR')
        MAIS_DE_2_SM_ATE_3_SM = MetaValue(3.0, 'RENDA_FAMILIAR')
        MAIS_DE_3_SM_ATE_5_SM = MetaValue(4.0, 'RENDA_FAMILIAR')
        MAIS_DE_5_SM_ATE_10_SM = MetaValue(5.0, 'RENDA_FAMILIAR')
        MAIS_DE_10_SM_ATE_20_SM = MetaValue(6.0, 'RENDA_FAMILIAR')
        MAIS_DE_20_SM_ATE_30_SM = MetaValue(7.0, 'RENDA_FAMILIAR')
        MAIS_DE_30_SM = MetaValue(8.0, 'RENDA_FAMILIAR')
        NAO_TEM_RENDA = MetaValue(9.0, 'RENDA_FAMILIAR')
        NAO_SABE = MetaValue(97.0, 'RENDA_FAMILIAR')
        NAO_RESPONDEU = MetaValue(98.0, 'RENDA_FAMILIAR')
        _map = {
            1.0: 'Até 1 SM',
            2.0: 'Mais de 1 SM até 2 SM',
            3.0: 'Mais de 2 SM até 3 SM',
            4.0: 'Mais de 3 SM até 5 SM',
            5.0: 'Mais de 5 SM até 10 SM',
            6.0: 'Mais de 10 SM até 20 SM',
            7.0: 'Mais de 20 SM até 30 SM',
            8.0: 'Mais de 30 SM',
            9.0: 'Não tem renda',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }


    class TV_ASSINATURA:
        """No domicílio tem tv por assinatura (a Cabo, Satélite etc.)?"""
        _label = 'No domicílio tem tv por assinatura (a Cabo, Satélite etc.)?'
        NAO_TEM = MetaValue(0.0, 'TV_ASSINATURA')
        TEM = MetaValue(1.0, 'TV_ASSINATURA')
        _map = {
            0.0: 'Não tem',
            1.0: 'Tem',
        }

    class ANTENA_PARABOLICA:
        """No domicílio tem antena parabólica?"""
        _label = 'No domicílio tem antena parabólica?'
        NAO_TEM = MetaValue(0.0, 'ANTENA_PARABOLICA')
        TEM = MetaValue(1.0, 'ANTENA_PARABOLICA')
        _map = {
            0.0: 'Não tem',
            1.0: 'Tem',
        }

    class RUA:
        """Tipo de pavimentação da rua"""
        _label = 'Tipo de pavimentação da rua'
        ASFALTADA_PAVIMENTADA = MetaValue(1.0, 'RUA')
        TERRA_CASCALHO = MetaValue(2.0, 'RUA')
        _map = {
            1.0: 'Asfaltada/Pavimentada',
            2.0: 'Terra/Cascalho',
        }

    class GRAU_INSTRUCAO:
        """Até que ano de escola o responsável pelo domicílio cursou?"""
        _label = 'Até que ano de escola o responsável pelo domicílio cursou?'
        ANALFABETO_ATE_3A_SERIE_FUNDAMENTAL = MetaValue(1.0, 'GRAU_INSTRUCAO')
        V_4A_A_7A_SERIE_FUNDAMENTAL = MetaValue(2.0, 'GRAU_INSTRUCAO')
        FUNDAMENTAL_COMPLETO_MEDIO_INCOMPLETO = MetaValue(3.0, 'GRAU_INSTRUCAO')
        MEDIO_COMPLETO_SUPERIOR_INCOMPLETO = MetaValue(4.0, 'GRAU_INSTRUCAO')
        SUPERIOR_COMPLETO = MetaValue(5.0, 'GRAU_INSTRUCAO')
        _map = {
            1.0: 'Analfabeto/ até 3ª Série Fundamental',
            2.0: '4ª a 7ª Série Fundamental',
            3.0: 'Fundamental completo/ Médio incompleto',
            4.0: 'Médio completo/ Superior incompleto',
            5.0: 'Superior completo',
        }

    class PNADC_RD_A:
        """Nos últimos três meses, alguma pessoa desse domicílio recebeu rendimentos de Benefício Assistencial de Prestação Continuada ou BPC-LOAS?"""
        _label = 'Nos últimos três meses, alguma pessoa desse domicílio recebeu rendimentos de Benefício Assistencial de Prestação Continuada ou BPC-LOAS?'
        NAO = MetaValue(0.0, 'PNADC_RD_A')
        SIM = MetaValue(1.0, 'PNADC_RD_A')
        NAO_SABE = MetaValue(97.0, 'PNADC_RD_A')
        NAO_RESPONDEU = MetaValue(98.0, 'PNADC_RD_A')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class PNADC_RD_B:
        """Nos últimos três meses, alguma pessoa desse domicílio recebeu rendimentos de Programa Bolsa Família ou Auxílio Brasil?"""
        _label = 'Nos últimos três meses, alguma pessoa desse domicílio recebeu rendimentos de Programa Bolsa Família ou Auxílio Brasil?'
        NAO = MetaValue(0.0, 'PNADC_RD_B')
        SIM = MetaValue(1.0, 'PNADC_RD_B')
        NAO_SABE = MetaValue(97.0, 'PNADC_RD_B')
        NAO_RESPONDEU = MetaValue(98.0, 'PNADC_RD_B')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class A1_A:
        """Neste domicílio tem Computador de mesa?"""
        _label = 'Neste domicílio tem Computador de mesa?'
        NAO = MetaValue(0.0, 'A1_A')
        SIM = MetaValue(1.0, 'A1_A')
        NAO_SABE = MetaValue(97.0, 'A1_A')
        NAO_RESPONDEU = MetaValue(98.0, 'A1_A')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class A1_B:
        """Neste domicílio tem notebook?"""
        _label = 'Neste domicílio tem notebook?'
        NAO = MetaValue(0.0, 'A1_B')
        SIM = MetaValue(1.0, 'A1_B')
        NAO_SABE = MetaValue(97.0, 'A1_B')
        NAO_RESPONDEU = MetaValue(98.0, 'A1_B')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class A1_C:
        """Neste domicílio tem Tablet?"""
        _label = 'Neste domicílio tem Tablet?'
        NAO = MetaValue(0.0, 'A1_C')
        SIM = MetaValue(1.0, 'A1_C')
        NAO_SABE = MetaValue(97.0, 'A1_C')
        NAO_RESPONDEU = MetaValue(98.0, 'A1_C')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class A2_QTD_DESK:
        """Quantos computadores de mesa têm neste domicílio?"""
        _label = 'Quantos computadores de mesa têm neste domicílio?'
        UM = MetaValue(1.0, 'A2_QTD_DESK')
        DOIS = MetaValue(2.0, 'A2_QTD_DESK')
        TRES = MetaValue(3.0, 'A2_QTD_DESK')
        QUATRO = MetaValue(4.0, 'A2_QTD_DESK')
        CINCO = MetaValue(5.0, 'A2_QTD_DESK')
        SEIS = MetaValue(6.0, 'A2_QTD_DESK')
        SETE = MetaValue(7.0, 'A2_QTD_DESK')
        OITO = MetaValue(8.0, 'A2_QTD_DESK')
        NAO_SE_APLICA = MetaValue(999999999.0, 'A2_QTD_DESK')
        _map = {
            1.0: 'Um',
            2.0: 'Dois',
            3.0: 'Três',
            4.0: 'Quatro',
            5.0: 'Cinco',
            6.0: 'Seis',
            7.0: 'Sete',
            8.0: 'Oito',
            999999999.0: 'Não se aplica',
        }

    class A2_QTD_NOTE:
        """Quantos notebooks têm neste domicílio?"""
        _label = 'Quantos notebooks têm neste domicílio?'
        UM = MetaValue(1.0, 'A2_QTD_NOTE')
        DOIS = MetaValue(2.0, 'A2_QTD_NOTE')
        TRES = MetaValue(3.0, 'A2_QTD_NOTE')
        QUATRO = MetaValue(4.0, 'A2_QTD_NOTE')
        CINCO = MetaValue(5.0, 'A2_QTD_NOTE')
        SEIS = MetaValue(6.0, 'A2_QTD_NOTE')
        SETE = MetaValue(7.0, 'A2_QTD_NOTE')
        OITO = MetaValue(8.0, 'A2_QTD_NOTE')
        NAO_SE_APLICA = MetaValue(999999999.0, 'A2_QTD_NOTE')
        _map = {
            1.0: 'Um',
            2.0: 'Dois',
            3.0: 'Três',
            4.0: 'Quatro',
            5.0: 'Cinco',
            6.0: 'Seis',
            7.0: 'Sete',
            8.0: 'Oito',
            999999999.0: 'Não se aplica',
        }

    class A2_QTD_TAB:
        """Quantos tablets têm neste domicílio?"""
        _label = 'Quantos tablets têm neste domicílio?'
        UM = MetaValue(1.0, 'A2_QTD_TAB')
        DOIS = MetaValue(2.0, 'A2_QTD_TAB')
        TRES = MetaValue(3.0, 'A2_QTD_TAB')
        QUATRO = MetaValue(4.0, 'A2_QTD_TAB')
        CINCO = MetaValue(5.0, 'A2_QTD_TAB')
        SEIS = MetaValue(6.0, 'A2_QTD_TAB')
        SETE = MetaValue(7.0, 'A2_QTD_TAB')
        OITO = MetaValue(8.0, 'A2_QTD_TAB')
        NAO_SE_APLICA = MetaValue(999999999.0, 'A2_QTD_TAB')
        _map = {
            1.0: 'Um',
            2.0: 'Dois',
            3.0: 'Três',
            4.0: 'Quatro',
            5.0: 'Cinco',
            6.0: 'Seis',
            7.0: 'Sete',
            8.0: 'Oito',
            999999999.0: 'Não se aplica',
        }

    class A4:
        """Este domicílio tem acesso à Internet?"""
        _label = 'Este domicílio tem acesso à Internet?'
        NAO = MetaValue(0.0, 'A4')
        SIM = MetaValue(1.0, 'A4')
        NAO_SABE = MetaValue(97.0, 'A4')
        NAO_RESPONDEU = MetaValue(98.0, 'A4')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class A5_A:
        """O domicílio não tem acesso à Internet, por falta de computador no domicílio?"""
        _label = 'O domicílio não tem acesso à Internet, por falta de computador no domicílio?'
        NAO = MetaValue(0.0, 'A5_A')
        SIM = MetaValue(1.0, 'A5_A')
        NAO_SABE = MetaValue(97.0, 'A5_A')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_A')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_A')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_B:
        """O domicílio não tem acesso à Internet, por falta de necessidade dos moradores?"""
        _label = 'O domicílio não tem acesso à Internet, por falta de necessidade dos moradores?'
        NAO = MetaValue(0.0, 'A5_B')
        SIM = MetaValue(1.0, 'A5_B')
        NAO_SABE = MetaValue(97.0, 'A5_B')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_B')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_B')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_C:
        """O domicílio não tem acesso à Internet, por falta de interesse dos moradores?"""
        _label = 'O domicílio não tem acesso à Internet, por falta de interesse dos moradores?'
        NAO = MetaValue(0.0, 'A5_C')
        SIM = MetaValue(1.0, 'A5_C')
        NAO_SABE = MetaValue(97.0, 'A5_C')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_C')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_C')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_D:
        """O domicílio não tem acesso à Internet, porque os moradores têm acesso à Internet em outro lugar?"""
        _label = 'O domicílio não tem acesso à Internet, porque os moradores têm acesso à Internet em outro lugar?'
        NAO = MetaValue(0.0, 'A5_D')
        SIM = MetaValue(1.0, 'A5_D')
        NAO_SABE = MetaValue(97.0, 'A5_D')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_D')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_D')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_E:
        """O domicílio não tem acesso à Internet, porque os moradores acham muito caro?"""
        _label = 'O domicílio não tem acesso à Internet, porque os moradores acham muito caro?'
        NAO = MetaValue(0.0, 'A5_E')
        SIM = MetaValue(1.0, 'A5_E')
        NAO_SABE = MetaValue(97.0, 'A5_E')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_E')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_E')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_F:
        """O domicílio não tem acesso à Internet, porque os moradores não sabem usar Internet?"""
        _label = 'O domicílio não tem acesso à Internet, porque os moradores não sabem usar Internet?'
        NAO = MetaValue(0.0, 'A5_F')
        SIM = MetaValue(1.0, 'A5_F')
        NAO_SABE = MetaValue(97.0, 'A5_F')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_F')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_F')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_G:
        """O domicílio não tem acesso à Internet, por falta de disponibilidade de Internet na região do domicílio?"""
        _label = 'O domicílio não tem acesso à Internet, por falta de disponibilidade de Internet na região do domicílio?'
        NAO = MetaValue(0.0, 'A5_G')
        SIM = MetaValue(1.0, 'A5_G')
        NAO_SABE = MetaValue(97.0, 'A5_G')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_G')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_G')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_H:
        """O domicílio não tem acesso à Internet, porque os moradores têm preocupações com segurança ou privacidade?"""
        _label = 'O domicílio não tem acesso à Internet, porque os moradores têm preocupações com segurança ou privacidade?'
        NAO = MetaValue(0.0, 'A5_H')
        SIM = MetaValue(1.0, 'A5_H')
        NAO_SABE = MetaValue(97.0, 'A5_H')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_H')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_H')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_I:
        """O domicílio não tem acesso à Internet, porque os moradores evitam o contato com conteúdo perigoso?"""
        _label = 'O domicílio não tem acesso à Internet, porque os moradores evitam o contato com conteúdo perigoso?'
        NAO = MetaValue(0.0, 'A5_I')
        SIM = MetaValue(1.0, 'A5_I')
        NAO_SABE = MetaValue(97.0, 'A5_I')
        NAO_RESPONDEU = MetaValue(98.0, 'A5_I')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_I')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A5_OUTRO:
        """O domicílio não tem acesso à Internet, por outro motivo?"""
        _label = 'O domicílio não tem acesso à Internet, por outro motivo?'
        NAO = MetaValue(0.0, 'A5_OUTRO')
        SIM = MetaValue(1.0, 'A5_OUTRO')
        NAO_SE_APLICA = MetaValue(99.0, 'A5_OUTRO')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            99.0: 'Não se aplica',
        }

    class A5A:
        """E qual desses motivos é o principal?"""
        _label = 'E qual desses motivos é o principal?'
        POR_FALTA_DE_COMPUTADOR_NO_DOMICILIO = MetaValue(1.0, 'A5A')
        POR_FALTA_DE_NECESSIDADE_DOS_MORADORES = MetaValue(2.0, 'A5A')
        POR_FALTA_DE_INTERESSE_DOS_MORADORES = MetaValue(3.0, 'A5A')
        PORQUE_OS_MORADORES_TEM_ACESSO_A_INTERNET_EM_OUTRO_LUGAR = MetaValue(4.0, 'A5A')
        PORQUE_OS_MORADORES_ACHAM_MUITO_CARO = MetaValue(5.0, 'A5A')
        PORQUE_OS_MORADORES_NAO_SABEM_USAR_INTERNET = MetaValue(6.0, 'A5A')
        POR_FALTA_DE_DISPONIBILIDADE_DE_INTERNET_NA_REGIAO_DO_DOMICILIO = MetaValue(7.0, 'A5A')
        PORQUE_OS_MORADORES_TEM_PREOCUPACOES_COM_SEGURANCA_OU_PRIVACIDADE = MetaValue(8.0, 'A5A')
        PORQUE_OS_MORADORES_EVITAM_O_CONTATO_COM_CONTEUDO_PERIGOSO = MetaValue(9.0, 'A5A')
        OUTRO_MOTIVO = MetaValue(10.0, 'A5A')
        NAO_SABE = MetaValue(97.0, 'A5A')
        NAO_RESPONDEU = MetaValue(98.0, 'A5A')
        NAO_SE_APLICA = MetaValue(99.0, 'A5A')
        _map = {
            1.0: 'Por falta de computador no domicílio',
            2.0: 'Por falta de necessidade dos moradores',
            3.0: 'Por falta de interesse dos moradores',
            4.0: 'Porque os moradores têm acesso à Internet em outro lugar',
            5.0: 'Porque os moradores acham muito caro',
            6.0: 'Porque os moradores não sabem usar Internet',
            7.0: 'Por falta de disponibilidade de Internet na região do domicílio',
            8.0: 'Porque os moradores têm preocupações com segurança ou privacidade',
            9.0: 'Porque os moradores evitam o contato com conteúdo perigoso',
            10.0: 'Outro motivo',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A7A:
        """Neste domicílio tem Wi-Fi?"""
        _label = 'Neste domicílio tem Wi-Fi?'
        NAO = MetaValue(0.0, 'A7A')
        SIM = MetaValue(1.0, 'A7A')
        NAO_SABE = MetaValue(97.0, 'A7A')
        NAO_RESPONDEU = MetaValue(98.0, 'A7A')
        NAO_SE_APLICA = MetaValue(99.0, 'A7A')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A7D:
        """Algum morador tem acesso à Internet no domicílio por meio de computador, tablet, telefone celular, televisão ou outro equipamento?"""
        _label = 'Algum morador tem acesso à Internet no domicílio por meio de computador, tablet, telefone celular, televisão ou outro equipamento?'
        NAO = MetaValue(0.0, 'A7D')
        SIM = MetaValue(1.0, 'A7D')
        NAO_SABE = MetaValue(97.0, 'A7D')
        NAO_RESPONDEU = MetaValue(98.0, 'A7D')
        NAO_SE_APLICA = MetaValue(99.0, 'A7D')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A7:
        """Qual o principal tipo de conexão utilizado para acessar a Internet no domicílio?"""
        _label = 'Qual o principal tipo de conexão utilizado para acessar a Internet no domicílio?'
        CONEXAO_DISCADA_QUE_DEIXA_A_LINHA_DE_TELEFONE_OCUPADA_DURANTE_O_USO = MetaValue(1.0, 'A7')
        CONEXAO_DSL_VIA_LINHA_TELEFONICA_QUE_NAO_DEIXA_A_LINHA_OCUPADA_DURANTE_O_USO = MetaValue(2.0, 'A7')
        CONEXAO_VIA_CABO_DE_TV_OU_FIBRA_OTICA = MetaValue(3.0, 'A7')
        CONEXAO_VIA_SINAL_DE_RADIO = MetaValue(4.0, 'A7')
        CONEXAO_VIA_SINAL_DE_SATELITE = MetaValue(5.0, 'A7')
        CONEXAO_MOVEL_VIA_MODEM_OU_CHIP_3G_OU_4G = MetaValue(6.0, 'A7')
        NAO_SABE = MetaValue(97.0, 'A7')
        NAO_RESPONDEU = MetaValue(98.0, 'A7')
        NAO_SE_APLICA = MetaValue(99.0, 'A7')
        _map = {
            1.0: 'Conexão discada, que deixa a linha de telefone ocupada durante o uso',
            2.0: 'Conexão DSL, via linha telefônica, que não deixa a linha ocupada durante o uso',
            3.0: 'Conexão via cabo de TV ou fibra ótica',
            4.0: 'Conexão via sinal de Rádio',
            5.0: 'Conexão via sinal de Satélite',
            6.0: 'Conexão móvel via modem ou chip 3G ou 4G',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A7C:
        """Essa conexão via rede móvel 3G, 4G ou 5G é acessada por meio de"""
        _label = 'Essa conexão via rede móvel 3G, 4G ou 5G é acessada por meio de'
        UM_TELEFONE_CELULAR = MetaValue(1.0, 'A7C')
        UM_MODEM_USB_CONECTADO_DIRETAMENTE_NO_COMPUTADOR_OU_UM_APARELHO_MODEM_LIGADO_NA_TOMADA = MetaValue(2.0, 'A7C')
        OUTRO_EQUIPAMENTO = MetaValue(3.0, 'A7C')
        NAO_SABE = MetaValue(97.0, 'A7C')
        NAO_RESPONDEU = MetaValue(98.0, 'A7C')
        NAO_SE_APLICA = MetaValue(99.0, 'A7C')
        _map = {
            1.0: 'Um telefone celular',
            2.0: 'Um modem USB conectado diretamente no computador ou um aparelho modem ligado na tomada',
            3.0: 'Outro equipamento',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A7B:
        """A Internet utilizada neste domicilio é utilizada também em algum domicílio vizinho?"""
        _label = 'A Internet utilizada neste domicilio é utilizada também em algum domicílio vizinho?'
        NAO = MetaValue(0.0, 'A7B')
        SIM = MetaValue(1.0, 'A7B')
        NAO_SABE = MetaValue(97.0, 'A7B')
        NAO_RESPONDEU = MetaValue(98.0, 'A7B')
        NAO_SE_APLICA = MetaValue(99.0, 'A7B')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A8A:
        """Considerando as seguintes faixas, qual é a velocidade da Internet contratada neste domicílio?"""
        _label = 'Considerando as seguintes faixas, qual é a velocidade da Internet contratada neste domicílio?'
        ATE_4_MEGAS_POR_SEGUNDO = MetaValue(1.0, 'A8A')
        DE_5_A_10_MEGAS_POR_SEGUNDO = MetaValue(2.0, 'A8A')
        DE_11_A_50_MEGAS_POR_SEGUNDO = MetaValue(3.0, 'A8A')
        DE_51_A_100_MEGAS_POR_SEGUNDO = MetaValue(4.0, 'A8A')
        DE_101_A_300_MEGAS_POR_SEGUNDO = MetaValue(5.0, 'A8A')
        DE_301_A_500_MEGAS_POR_SEGUNDO = MetaValue(6.0, 'A8A')
        V_501_MEGAS_POR_SEGUNDO_OU_MAIS = MetaValue(7.0, 'A8A')
        NAO_SABE = MetaValue(97.0, 'A8A')
        NAO_RESPONDEU = MetaValue(98.0, 'A8A')
        NAO_SE_APLICA = MetaValue(99.0, 'A8A')
        _map = {
            1.0: 'Até 4 megas por segundo',
            2.0: 'De 5 a 10 megas por segundo',
            3.0: 'De 11 a 50 megas por segundo',
            4.0: 'De 51 a 100 megas por segundo',
            5.0: 'De 101 a 300 megas por segundo',
            6.0: 'De 301 a 500 megas por segundo',
            7.0: '501 megas por segundo ou mais',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A9A:
        """Qual o valor aproximadamente pago pela Internet contratada no domicílio?"""
        _label = 'Qual o valor aproximadamente pago pela Internet contratada no domicílio?'
        NAO_PAGA_NADA = MetaValue(0.0, 'A9A')
        ATE_R_10 = MetaValue(1.0, 'A9A')
        DE_R_11_A_R_20 = MetaValue(2.0, 'A9A')
        DE_R_21_A_R_30 = MetaValue(3.0, 'A9A')
        DE_R_31_A_R_40 = MetaValue(4.0, 'A9A')
        DE_R_41_A_R_50 = MetaValue(5.0, 'A9A')
        DE_R_51_A_R_60 = MetaValue(6.0, 'A9A')
        DE_R_61_A_R_70 = MetaValue(7.0, 'A9A')
        DE_R_71_A_R_80 = MetaValue(8.0, 'A9A')
        DE_R_81_A_R_90 = MetaValue(9.0, 'A9A')
        DE_R_91_A_R_100 = MetaValue(10.0, 'A9A')
        DE_R_101_A_R_110 = MetaValue(11.0, 'A9A')
        DE_R_111_A_R_120 = MetaValue(12.0, 'A9A')
        DE_R_121_A_R_130 = MetaValue(13.0, 'A9A')
        DE_R_131_A_R_140 = MetaValue(14.0, 'A9A')
        DE_R_141_A_R_150 = MetaValue(15.0, 'A9A')
        ACIMA_DE_R_150 = MetaValue(16.0, 'A9A')
        NAO_PAGA_NADA = MetaValue(17.0, 'A9A')
        NAO_SABE = MetaValue(97.0, 'A9A')
        NAO_RESPONDEU = MetaValue(98.0, 'A9A')
        NAO_SE_APLICA = MetaValue(99.0, 'A9A')
        _map = {
            0.0: 'Não paga nada',
            1.0: 'Até R$ 10',
            2.0: 'De R$11 a R$ 20',
            3.0: 'De R$21 a R$ 30',
            4.0: 'De R$31 a R$ 40',
            5.0: 'De R$41 a R$ 50',
            6.0: 'De R$51 a R$ 60',
            7.0: 'De R$61 a R$ 70',
            8.0: 'De R$71 a R$ 80',
            9.0: 'De R$81 a R$ 90',
            10.0: 'De R$91 a R$ 100',
            11.0: 'De R$101 a R$ 110',
            12.0: 'De R$111 a R$ 120',
            13.0: 'De R$121 a R$ 130',
            14.0: 'De R$131 a R$ 140',
            15.0: 'De R$141 a R$ 150',
            16.0: 'Acima de R$ 150',
            17.0: 'Não paga nada',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A9B:
        """Esse valor refere-se a um pacote ou combo que inclui outros serviços, como telefone fixo ou canais de TV por assinatura, por exemplo?"""
        _label = 'Esse valor refere-se a um pacote ou combo que inclui outros serviços, como telefone fixo ou canais de TV por assinatura, por exemplo?'
        NAO = MetaValue(0.0, 'A9B')
        SIM = MetaValue(1.0, 'A9B')
        NAO_SABE = MetaValue(97.0, 'A9B')
        NAO_RESPONDEU = MetaValue(98.0, 'A9B')
        NAO_SE_APLICA = MetaValue(99.0, 'A9B')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }

    class A9C:
        """E o(a) sr(a) sabe o valor apenas da Internet?"""
        _label = 'E o(a) sr(a) sabe o valor apenas da Internet?'
        NAO = MetaValue(0.0, 'A9C')
        SIM = MetaValue(1.0, 'A9C')
        NAO_SE_APLICA = MetaValue(99.0, 'A9C')
        _map = {
            0.0: 'Não',
            1.0: 'Sim',
            99.0: 'Não se aplica',
        }

    class A9D:
        """E qual o valor pago aproximadamente apenas pela Internet contratada neste domicílio?"""
        _label = 'E qual o valor pago aproximadamente apenas pela Internet contratada neste domicílio?'
        NAO_PAGA_NADA = MetaValue(0.0, 'A9D')
        ATE_R_10 = MetaValue(1.0, 'A9D')
        DE_R_11_A_R_20 = MetaValue(2.0, 'A9D')
        DE_R_21_A_R_30 = MetaValue(3.0, 'A9D')
        DE_R_31_A_R_40 = MetaValue(4.0, 'A9D')
        DE_R_41_A_R_50 = MetaValue(5.0, 'A9D')
        DE_R_51_A_R_60 = MetaValue(6.0, 'A9D')
        DE_R_61_A_R_70 = MetaValue(7.0, 'A9D')
        DE_R_71_A_R_80 = MetaValue(8.0, 'A9D')
        DE_R_81_A_R_90 = MetaValue(9.0, 'A9D')
        DE_R_91_A_R_100 = MetaValue(10.0, 'A9D')
        DE_R_101_A_R_110 = MetaValue(11.0, 'A9D')
        DE_R_111_A_R_120 = MetaValue(12.0, 'A9D')
        DE_R_121_A_R_130 = MetaValue(13.0, 'A9D')
        DE_R_131_A_R_140 = MetaValue(14.0, 'A9D')
        DE_R_141_A_R_150 = MetaValue(15.0, 'A9D')
        ACIMA_DE_R_150 = MetaValue(16.0, 'A9D')
        NAO_PAGA_NADA = MetaValue(17.0, 'A9D')
        NAO_SABE = MetaValue(97.0, 'A9D')
        NAO_RESPONDEU = MetaValue(98.0, 'A9D')
        NAO_SE_APLICA = MetaValue(99.0, 'A9D')
        _map = {
            0.0: 'Não paga nada',
            1.0: 'Até R$ 10',
            2.0: 'De R$11 a R$ 20',
            3.0: 'De R$21 a R$ 30',
            4.0: 'De R$31 a R$ 40',
            5.0: 'De R$41 a R$ 50',
            6.0: 'De R$51 a R$ 60',
            7.0: 'De R$61 a R$ 70',
            8.0: 'De R$71 a R$ 80',
            9.0: 'De R$81 a R$ 90',
            10.0: 'De R$91 a R$ 100',
            11.0: 'De R$101 a R$ 110',
            12.0: 'De R$111 a R$ 120',
            13.0: 'De R$121 a R$ 130',
            14.0: 'De R$131 a R$ 140',
            15.0: 'De R$141 a R$ 150',
            16.0: 'Acima de R$ 150',
            17.0: 'Não paga nada',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
            99.0: 'Não se aplica',
        }


    class COD_REGIAO_2:
        """Região"""
        _label = 'Região'
        SUDESTE = MetaValue(1.0, 'COD_REGIAO_2')
        NORDESTE = MetaValue(2.0, 'COD_REGIAO_2')
        SUL = MetaValue(3.0, 'COD_REGIAO_2')
        NORTE = MetaValue(4.0, 'COD_REGIAO_2')
        CENTRO_OESTE = MetaValue(5.0, 'COD_REGIAO_2')
        _map = {
            1.0: 'Sudeste',
            2.0: 'Nordeste',
            3.0: 'Sul',
            4.0: 'Norte',
            5.0: 'Centro-Oeste',
        }

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
        _map = {
            1.0: 'Até 1 SM',
            2.0: 'Mais de 1 SM até 2 SM',
            3.0: 'Mais de 2 SM até 3 SM',
            4.0: 'Mais de 3 SM até 5 SM',
            5.0: 'Mais de 5 SM até 10 SM',
            6.0: 'Mais de 10 SM',
            7.0: 'Não tem renda',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

    class CLASSE_2015:
        """Classe social"""
        _label = 'Classe social'
        A = MetaValue(1.0, 'CLASSE_2015')
        B = MetaValue(2.0, 'CLASSE_2015')
        C = MetaValue(3.0, 'CLASSE_2015')
        DE = MetaValue(4.0, 'CLASSE_2015')
        _map = {
            1.0: 'A',
            2.0: 'B',
            3.0: 'C',
            4.0: 'DE',
        }

    class A1_AGREG:
        """Domicílios com computador"""
        _label = 'Domicílios com computador'
        SIM = MetaValue(1.0, 'A1_AGREG')
        NAO = MetaValue(0.0, 'A1_AGREG')
        _map = {
            1.0: 'Sim',
            0.0: 'Não',
        }

    class DIC_CEL:
        """Domicílios que possuem equipamentos TIC"""
        _label = 'Domicílios que possuem equipamentos TIC'
        TELEFONE_CELULAR = MetaValue(1.0, 'DIC_CEL')
        _map = {
            1.0: 'Telefone celular',
        }

    class A1_EXCLUSIVOS:
        """Domicílios com computador, por tipo de computador presente de forma exclusiva ou simultânea no domicílio"""
        _label = 'Domicílios com computador, por tipo de computador presente de forma exclusiva ou simultânea no domicílio'
        APENAS_COMPUTADOR_DE_MESA = MetaValue(1.0, 'A1_EXCLUSIVOS')
        APENAS_NOTEBOOK = MetaValue(2.0, 'A1_EXCLUSIVOS')
        APENAS_TABLET = MetaValue(3.0, 'A1_EXCLUSIVOS')
        MAIS_DE_UM_TIPO_DE_COMPUTADOR = MetaValue(99.0, 'A1_EXCLUSIVOS')
        _map = {
            1.0: 'Apenas computador de mesa',
            2.0: 'Apenas notebook',
            3.0: 'Apenas tablet',
            99.0: 'Mais de um tipo de computador',
        }

    class A2_A_FAIXA:
        """Faixa de quantidade - Computador de mesa"""
        _label = 'Faixa de quantidade - Computador de mesa'
        NENHUM = MetaValue(0.0, 'A2_A_FAIXA')
        UM = MetaValue(1.0, 'A2_A_FAIXA')
        DOIS_OU_MAIS = MetaValue(2.0, 'A2_A_FAIXA')
        _map = {
            0.0: 'Nenhum',
            1.0: 'Um',
            2.0: 'Dois ou mais',
        }

    class A2_B_FAIXA:
        """Faixa de quantidade - Notebook"""
        _label = 'Faixa de quantidade - Notebook'
        NENHUM = MetaValue(0.0, 'A2_B_FAIXA')
        UM = MetaValue(1.0, 'A2_B_FAIXA')
        DOIS_OU_MAIS = MetaValue(2.0, 'A2_B_FAIXA')
        _map = {
            0.0: 'Nenhum',
            1.0: 'Um',
            2.0: 'Dois ou mais',
        }

    class A2_C_FAIXA:
        """Faixa de quantidade - Tablet"""
        _label = 'Faixa de quantidade - Tablet'
        NENHUM = MetaValue(0.0, 'A2_C_FAIXA')
        UM = MetaValue(1.0, 'A2_C_FAIXA')
        DOIS_OU_MAIS = MetaValue(2.0, 'A2_C_FAIXA')
        _map = {
            0.0: 'Nenhum',
            1.0: 'Um',
            2.0: 'Dois ou mais',
        }

    class A4_COB:
        """Domicilio com acesso a internet - ampliado"""
        _label = 'Domicilio com acesso a internet - ampliado'
        SIM = MetaValue(1.0, 'A4_COB')
        NAO = MetaValue(0.0, 'A4_COB')
        _map = {
            1.0: 'Sim',
            0.0: 'Não',
        }

    class A1A4:
        """Domicílios por presença de computador e Internet"""
        _label = 'Domicílios por presença de computador e Internet'
        AMBOS = MetaValue(1.0, 'A1A4')
        APENAS_COMPUTADOR = MetaValue(2.0, 'A1A4')
        APENAS_INTERNET = MetaValue(3.0, 'A1A4')
        NEM_COMPUTADOR_NEM_INTERNET = MetaValue(4.0, 'A1A4')
        _map = {
            1.0: 'Ambos',
            2.0: 'Apenas computador',
            3.0: 'Apenas Internet',
            4.0: 'Nem computador nem Internet',
        }

    class A7_AGREG:
        """Domicílios com acesso à Internet, por tipo de conexão"""
        _label = 'Domicílios com acesso à Internet, por tipo de conexão'
        TOTAL_BANDA_LARGA_FIXA = MetaValue(1.0, 'A7_AGREG')
        _map = {
            1.0: 'Total - Banda larga fixa',
        }

    class A5_NENHUM:
        """Domicílios sem acesso à Internet, por motivos para a falta de Internet"""
        _label = 'Domicílios sem acesso à Internet, por motivos para a falta de Internet'
        NENHUM_DESSES_MOTIVOS = MetaValue(1.0, 'A5_NENHUM')
        _map = {
            1.0: 'Nenhum desses motivos',
        }

    class A9_FAIXA:
        """Domicílios com acesso à Internet, por valor pago pela principal conexão"""
        _label = 'Domicílios com acesso à Internet, por valor pago pela principal conexão'
        ATE_R_30 = MetaValue(1.0, 'A9_FAIXA')
        R_31_A_R_40 = MetaValue(2.0, 'A9_FAIXA')
        R_41_A_R_50 = MetaValue(3.0, 'A9_FAIXA')
        R_51_A_R_60 = MetaValue(4.0, 'A9_FAIXA')
        R_61_A_R_70 = MetaValue(5.0, 'A9_FAIXA')
        R_71_A_R_80 = MetaValue(6.0, 'A9_FAIXA')
        R_81_A_R_90 = MetaValue(7.0, 'A9_FAIXA')
        R_91_A_R_100 = MetaValue(8.0, 'A9_FAIXA')
        R_101_A_R_150 = MetaValue(9.0, 'A9_FAIXA')
        MAIS_DE_R_150 = MetaValue(10.0, 'A9_FAIXA')
        NAO_SABE = MetaValue(97.0, 'A9_FAIXA')
        NAO_RESPONDEU = MetaValue(98.0, 'A9_FAIXA')
        _map = {
            1.0: 'Até R$ 30',
            2.0: 'R$ 31 a R$ 40',
            3.0: 'R$ 41 a R$ 50',
            4.0: 'R$ 51 a R$ 60',
            5.0: 'R$ 61 a R$ 70',
            6.0: 'R$ 71 a R$ 80',
            7.0: 'R$ 81 a R$ 90',
            8.0: 'R$ 91 a R$ 100',
            9.0: 'R$ 101 a R$ 150',
            10.0: 'Mais de R$ 150',
            97.0: 'Não sabe',
            98.0: 'Não respondeu',
        }

