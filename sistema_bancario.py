import textwrap


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato):
    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato

    saldo += valor
    extrato += f"Depósito:\tR$ {valor:.2f}\n"
    print("\n=== Depósito realizado com sucesso! ===")
    return saldo, extrato


def sacar(saldo, valor, extrato, limite, numero_saques, limite_saques, cheque_especial):
    saldo_disponivel = saldo + cheque_especial

    if valor <= 0:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        return saldo, extrato, numero_saques

    if numero_saques >= limite_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > saldo_disponivel:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente, nem limite no cheque especial. @@@")

    else:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1

        if saldo < 0:
            print("\n=== Você utilizou seu cheque especial! ===")

        print("\n=== Saque realizado com sucesso! ===")

    return saldo, extrato, numero_saques


def exibir_extrato(saldo, extrato, cheque_especial):
    saldo_disponivel = saldo + cheque_especial
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo real:\t\tR$ {saldo:.2f}")
    print(f"Saldo disponível (com cheque especial): R$ {saldo_disponivel:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    if filtrar_usuario(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    return next((usuario for usuario in usuarios if usuario["cpf"] == cpf), None)


def criar_conta(agencia, numero_conta, usuarios, cheque_especial):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario, "cheque_especial": cheque_especial}

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
    return None


def listar_contas(contas):
    if not contas:
        print("\n@@@ Não há contas para listar! @@@")
        return

    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Cheque Especial:\tR$ {conta['cheque_especial']:.2f}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    CHEQUE_ESPECIAL_PADRAO = 1000  # Valor fixo de cheque especial para cada conta

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            # Obter o cheque especial da conta
            cheque_especial = CHEQUE_ESPECIAL_PADRAO

            saldo, extrato, numero_saques = sacar(
                saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES, cheque_especial
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato, CHEQUE_ESPECIAL_PADRAO)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios, CHEQUE_ESPECIAL_PADRAO)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main()
