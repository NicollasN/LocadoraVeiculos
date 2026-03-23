# Sistema de locadora de veículos
import sqlite3

def criar_banco():
    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()

    # Criar tabela de veículos
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS veiculos (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         marca TEXT NOT NULL,
    #         modelo TEXT NOT NULL,
    #         ano INTEGER NOT NULL,
    #         disponivel BOOLEAN NOT NULL
    #     )
    # ''')

    # # Criar tabela de clientes
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS clientes (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         cpf TEXT UNIQUE NOT NULL,
    #         nome TEXT NOT NULL,
    #         email TEXT NOT NULL
    #     )
    # ''')

    # # Criar tabela de locações
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS locacoes (
    #         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         cliente_id INTEGER NOT NULL,
    #         veiculo_id INTEGER NOT NULL,
    #         data_inicio TEXT NOT NULL,
    #         data_fim TEXT NOT NULL,
    #         FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    #         FOREIGN KEY (veiculo_id) REFERENCES veiculos(id)
    #     )
    # ''')

    conn.commit()
    conn.close()
    print("Banco de dados 'locadora.db' e tabelas criados/verificados com sucesso!")

# Funções do sistema
def menu():
    print("\nMenu:")
    print("1. Cadastrar veículo")
    print("2. Cadastrar cliente")
    print("3. Realizar locação")
    print("4. Listar veículos disponíveis")
    print("5. Listar clientes")
    print("6. Sair")

def cadastrar_veiculo():
    marca = input("Digite a marca do veículo: ")
    modelo = input("Digite o modelo do veículo: ")
    ano = int(input("Digite o ano do veículo: "))
    disponivel = True

    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO veiculos (marca, modelo, ano, disponivel)
        VALUES (?, ?, ?, ?)
    ''', (marca, modelo, ano, disponivel))
    conn.commit()
    conn.close()
    print(f"Veículo {marca} {modelo} cadastrado com sucesso!")

def cadastrar_cliente():
    cpf = input("Digite o CPF do cliente (apenas números): ")
    nome = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")

    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO clientes (cpf, nome, email)
            VALUES (?, ?, ?)
        ''', (cpf, nome, email))
        conn.commit()
        print(f"Cliente {nome} cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já cadastrado. Por favor, insira um CPF único.")
    finally:
        conn.close()

def realizar_locacao():
    cliente_id = int(input("Digite o ID do cliente: "))
    veiculo_id = int(input("Digite o ID do veículo: "))
    data_inicio = input("Digite a data de início (YYYY-MM-DD): ")
    data_fim = input("Digite a data de fim (YYYY-MM-DD): ")

    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()
    try:
        # Verificar se o veículo está disponível
        cursor.execute("SELECT disponivel FROM veiculos WHERE id = ?", (veiculo_id,))
        disponivel = cursor.fetchone()

        if disponivel and disponivel[0]:
            cursor.execute('''
                INSERT INTO locacoes (cliente_id, veiculo_id, data_inicio, data_fim)
                VALUES (?, ?, ?, ?)
            ''', (cliente_id, veiculo_id, data_inicio, data_fim))
            # Atualizar status do veículo para indisponível
            cursor.execute("UPDATE veiculos SET disponivel = 0 WHERE id = ?", (veiculo_id,))
            conn.commit()
            print("Locação realizada com sucesso!")
        else:
            print("Erro: Veículo não encontrado ou não disponível para locação.")
    except Exception as e:
        print(f"Erro ao realizar locação: {e}")
        conn.rollback() # Desfaz as operações em caso de erro
    finally:
        conn.close()

def listar_veiculos_disponiveis():
    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, marca, modelo, ano FROM veiculos WHERE disponivel = 1
    ''')
    veiculos = cursor.fetchall()
    conn.close()

    if veiculos:
        print("\nVeículos disponíveis:")
        for veiculo in veiculos:
            print(f"ID: {veiculo[0]}, Marca: {veiculo[1]}, Modelo: {veiculo[2]}, Ano: {veiculo[3]}")
    else:
        print("Nenhum veículo disponível no momento.")

def listar_clientes():
    conn = sqlite3.connect('locadora.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, cpf, nome, email FROM clientes
    ''')
    clientes = cursor.fetchall()
    conn.close()

    if clientes:
        print("\nClientes cadastrados:")
        for cliente in clientes:
            print(f"ID: {cliente[0]}, CPF: {cliente[1]}, Nome: {cliente[2]}, Email: {cliente[3]}")
    else:
        print("Nenhum cliente cadastrado.")

def sair():
    print("Saindo do sistema. Até logo!")
    # Não usamos exit() aqui para permitir um encerramento mais limpo do script

# --- Início do Programa Principal ---
if __name__ == '__main__':
    criar_banco() # Garante que o banco e tabelas existam

    print("Bem-vindo à Locadora de Veículos!")

    while True:
        menu()
        try:
            escolha = int(input("Escolha uma opção: "))
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            continue

        match escolha:
            case 1:
                cadastrar_veiculo()
            case 2:
                cadastrar_cliente()
            case 3:
                realizar_locacao()
            case 4:
                listar_veiculos_disponiveis()
            case 5:
                listar_clientes()
            case 6:
                sair()
                break # Sai do loop while True
            case _:
                print("Opção inválida. Por favor, escolha uma opção entre 1 e 6.")
