import datetime

# ESTRUTURAS DE DADOS (CLASSES)
class Empregado:
    def __init__(self, numero_funcional, nome, salario):
        self.numero_funcional = numero_funcional
        self.nome = nome
        self.salario = salario

class Projeto:
    def __init__(self, nome, data_inicio, data_termino, tempo_estimado_meses, valor_estimado, func_responsavel):
        self.nome = nome
        self.data_inicio = data_inicio
        self.data_termino = data_termino  # None significa que ainda está em andamento
        self.tempo_estimado_meses = tempo_estimado_meses
        self.valor_estimado = valor_estimado
        self.func_responsavel = func_responsavel

# ALGORITMOS DE BUSCA E ORDENAÇÃO

# 1. Busca Binária (O(log n)) - Melhor que O(n)
def busca_binaria_empregado(vetor, num_funcional):
    inicio = 0
    fim = len(vetor) - 1
    
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if vetor[meio].numero_funcional == num_funcional:
            return meio  # Retorna o índice
        elif vetor[meio].numero_funcional < num_funcional:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

def busca_binaria_projeto(vetor, nome_projeto):
    inicio = 0
    fim = len(vetor) - 1
    
    while inicio <= fim:
        meio = (inicio + fim) // 2
        if vetor[meio].nome == nome_projeto:
            return meio
        elif vetor[meio].nome < nome_projeto:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1

# 2. Bubble Sort (O(n^2)) - Para salários > 10.000 em ordem decrescente
def bubble_sort_salarios(vetor):
    n = len(vetor)
    for i in range(n):
        for j in range(0, n - i - 1):
            if vetor[j].salario < vetor[j + 1].salario:
                vetor[j], vetor[j + 1] = vetor[j + 1], vetor[j]
    return vetor

# 3. Merge Sort (O(n log n) que é <= n log^2 n)
def merge_sort_projetos_valor(vetor):
    if len(vetor) > 1:
        meio = len(vetor) // 2
        esq = vetor[:meio]
        dir = vetor[meio:]

        merge_sort_projetos_valor(esq)
        merge_sort_projetos_valor(dir)

        i = j = k = 0
        # Ordenando de forma crescente pelo valor
        while i < len(esq) and j < len(dir):
            if esq[i].valor_estimado <= dir[j].valor_estimado:
                vetor[k] = esq[i]
                i += 1
            else:
                vetor[k] = dir[j]
                j += 1
            k += 1

        while i < len(esq):
            vetor[k] = esq[i]
            i += 1
            k += 1

        while j < len(dir):
            vetor[k] = dir[j]
            j += 1
            k += 1
    return vetor

# 4. Insertion Sort - Para ordenar pelo tempo de atraso
def insertion_sort_atraso(vetor_tuplas):
    # vetor_tuplas tem o formato: (projeto, status, dias_atraso)
    for i in range(1, len(vetor_tuplas)):
        chave = vetor_tuplas[i]
        j = i - 1
        # Ordena decrescente pelo tempo de atraso (quem atrasou mais primeiro)
        while j >= 0 and chave[2] > vetor_tuplas[j][2]:
            vetor_tuplas[j + 1] = vetor_tuplas[j]
            j -= 1
        vetor_tuplas[j + 1] = chave
    return vetor_tuplas

# 5. Selection Sort - Para ordenar nomes dos funcionários em ordem alfabética
def selection_sort_nomes(vetor_nomes):
    n = len(vetor_nomes)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if vetor_nomes[j] < vetor_nomes[min_idx]:
                min_idx = j
        vetor_nomes[i], vetor_nomes[min_idx] = vetor_nomes[min_idx], vetor_nomes[i]
    return vetor_nomes

# FUNÇÕES DE MANUTENÇÃO DOS VETORES

def inserir_empregado_ordenado(vetor, empregado):
    if len(vetor) >= 500:
        print("Erro: Limite de 500 funcionários atingido.")
        return
    
    if busca_binaria_empregado(vetor, empregado.numero_funcional) != -1:
        print("Erro: Número funcional já existe!")
        return

    vetor.append(empregado)
    # Move o empregado para a posição correta (Insertion Sort)
    i = len(vetor) - 1
    while i > 0 and vetor[i - 1].numero_funcional > vetor[i].numero_funcional:
        vetor[i], vetor[i - 1] = vetor[i - 1], vetor[i]
        i -= 1
    print("Empregado cadastrado com sucesso!")

def inserir_projeto_ordenado(vetor, projeto):
    if len(vetor) >= 2000:
        print("Erro: Limite de 2000 projetos atingido.")
        return
        
    if busca_binaria_projeto(vetor, projeto.nome) != -1:
        print("Erro: Já existe um projeto com este nome!")
        return

    vetor.append(projeto)
    i = len(vetor) - 1
    while i > 0 and vetor[i - 1].nome > vetor[i].nome:
        vetor[i], vetor[i - 1] = vetor[i - 1], vetor[i]
        i -= 1
    print("Projeto cadastrado com sucesso!")

def remover_empregado(vetor, num_funcional):
    idx = busca_binaria_empregado(vetor, num_funcional)
    if idx != -1:
        # Desloca todos uma posição pra esquerda para remover
        for i in range(idx, len(vetor) - 1):
            vetor[i] = vetor[i + 1]
        vetor.pop()
        print("Empregado removido com sucesso!")
    else:
        print("Empregado não encontrado.")

def remover_projeto(vetor, nome):
    idx = busca_binaria_projeto(vetor, nome)
    if idx != -1:
        for i in range(idx, len(vetor) - 1):
            vetor[i] = vetor[i + 1]
        vetor.pop()
        print("Projeto removido com sucesso!")
    else:
        print("Projeto não encontrado.")

# TABELA HASH ESTÁTICA PARA E-MAILS DE GERENTES
class TabelaHash:
    def __init__(self, tamanho=100):
        self.tamanho = tamanho
        self.tabela = [None] * tamanho

    def _hash(self, email):
        soma = 0
        for char in email:
            soma += ord(char)
        return soma % self.tamanho

    def inserir(self, email):
        indice = self._hash(email)
        original = indice
        # Sondagem linear para resolver colisão
        while self.tabela[indice] is not None:
            if self.tabela[indice] == email:
                return # já existe
            indice = (indice + 1) % self.tamanho
            if indice == original:
                print("Erro: Tabela Hash cheia!")
                return
        self.tabela[indice] = email

    def imprimir_todos(self):
        print("\n--- E-mails dos Gerentes (Tabela Hash) ---")
        for e in self.tabela:
            if e is not None:
                print(e)

# FUNÇÕES DE DATA (Auxiliares)
def string_para_data(data_str):
    if not data_str:
        return None
    try:
        return datetime.datetime.strptime(data_str, "%d/%m/%Y")
    except:
        return None

# MAIN E MENU
def main():
    empregados = []
    projetos = []
    hash_emails = TabelaHash()

    # Dados mockados pra facilitar teste sem ter q digitar tudo sempre
    inserir_empregado_ordenado(empregados, Empregado(10, "Ana", 15000))
    inserir_empregado_ordenado(empregados, Empregado(2, "Carlos", 8000))
    inserir_empregado_ordenado(empregados, Empregado(5, "Beatriz", 12000))
    
    dt_inicio = datetime.datetime.now() - datetime.timedelta(days=100)
    dt_fim = datetime.datetime.now() - datetime.timedelta(days=10)
    inserir_projeto_ordenado(projetos, Projeto("Alpha", dt_inicio, None, 2, 600000, 10))
    inserir_projeto_ordenado(projetos, Projeto("Beta", dt_inicio, dt_fim, 1, 400000, 2))

    while True:
        print("\n" + "="*40)
        print("SISTEMA DE GESTÃO - ESTRUTURA DE DADOS")
        print("="*40)
        print("1. Cadastrar Empregado")
        print("2. Alterar Empregado")
        print("3. Remover Empregado")
        print("4. Cadastrar Projeto")
        print("5. Alterar Projeto")
        print("6. Remover Projeto")
        print("7. Buscar Empregado (Busca Binária)")
        print("8. Relatório: Salários > 10.000 (Bubble Sort)")
        print("9. Relatório: Projetos em Andamento > 500k (Merge Sort)")
        print("10. Relatório: Projetos Atrasados")
        print("11. Relatório: Bônus Responsáveis (Ordenação Alfabética)")
        print("12. Gerenciar E-mails de Gerentes (Hash)")
        print("0. Sair")
        print("="*40)
        
        opcao = input("Opção: ")

        if opcao == '0':
            break

        elif opcao == '1':
            num = int(input("Número Funcional: "))
            nome = input("Nome: ")
            sal = float(input("Salário: "))
            inserir_empregado_ordenado(empregados, Empregado(num, nome, sal))

        elif opcao == '2':
            num = int(input("Número Funcional do empregado a alterar (A chave não muda): "))
            idx = busca_binaria_empregado(empregados, num)
            if idx != -1:
                option = int(input("1 - Alterar Nome | 2 - Alterar Salário | 3 - Alterar Nome e Salário: "))
                if option == 1: empregados[idx].nome = input("Novo Nome: ")
                elif option == 2: empregados[idx].salario = float(input("Novo Salário: "))
                elif option == 3: 
                    empregados[idx].nome = input("Novo Nome: ")
                    empregados[idx].salario = float(input("Novo Salário: "))
            else:
                print("Empregado não encontrado.")

        elif opcao == '3':
            num = int(input("Número Funcional para remover: "))
            remover_empregado(empregados, num)

        elif opcao == '4':
            nome = input("Nome do Projeto: ")
            dt_in = string_para_data(input("Data Início (DD/MM/AAAA): "))
            dt_fim_str = input("Data Término (DD/MM/AAAA ou deixe em branco se em andamento): ")
            dt_fim = string_para_data(dt_fim_str) if dt_fim_str else None
            meses = int(input("Tempo estimado (meses): "))
            valor = float(input("Valor estimado: "))
            resp = int(input("Número funcional do responsável: "))
            inserir_projeto_ordenado(projetos, Projeto(nome, dt_in, dt_fim, meses, valor, resp))

        elif opcao == '5':
            nome = input("Nome do projeto a alterar (A chave não muda): ")
            idx = busca_binaria_projeto(projetos, nome)
            if idx != -1:
                projetos[idx].valor_estimado = float(input("Novo Valor Estimado: "))
                dt_fim_str = input("Nova Data de Término (DD/MM/AAAA ou branco se andamento): ")
                projetos[idx].data_termino = string_para_data(dt_fim_str) if dt_fim_str else None
                print("Projeto alterado!")
            else:
                print("Projeto não encontrado.")

        elif opcao == '6':
            nome = input("Nome do Projeto para remover: ")
            remover_projeto(projetos, nome)

        elif opcao == '7':
            num = int(input("Digite o Número Funcional: "))
            idx = busca_binaria_empregado(empregados, num)
            if idx != -1:
                e = empregados[idx]
                print(f"Encontrado: {e.nome} | Salário: R${e.salario:.2f}")
            else:
                print("Funcionário não encontrado.")

        elif opcao == '8':
            # Cria vetor auxiliar para não zoar a ordenação do original pelo numero funcional
            ricos = []
            for e in empregados:
                if e.salario > 10000:
                    ricos.append(e)
            
            ricos_ordenados = bubble_sort_salarios(ricos)
            print("\n--- Salários > R$10.000 (Ordem Decrescente) ---")
            for r in ricos_ordenados:
                print(f"{r.nome} - R${r.salario:.2f}")

        elif opcao == '9':
            caros_andamento = []
            for p in projetos:
                if p.data_termino is None and p.valor_estimado > 500000:
                    caros_andamento.append(p)
            
            projetos_ordenados = merge_sort_projetos_valor(caros_andamento)
            print("\n--- Projetos em Andamento > R$500.000 ---")
            for p in projetos_ordenados:
                print(f"{p.nome} - R${p.valor_estimado:.2f}")

        elif opcao == '10':
            atrasados = []
            hoje = datetime.datetime.now()
            
            for p in projetos:
                if not p.data_inicio: continue
                prazo_dias = p.tempo_estimado_meses * 30 
                data_esperada_fim = p.data_inicio + datetime.timedelta(days=prazo_dias)
                
                if p.data_termino is None:
                    dias_atraso = (hoje - data_esperada_fim).days
                    if dias_atraso > 0:
                        atrasados.append((p, "Em aberto", dias_atraso))
                else:
                    dias_atraso = (p.data_termino - data_esperada_fim).days
                    if dias_atraso > 0:
                        atrasados.append((p, "Finalizado", dias_atraso))
            
            atrasados_ordenados = insertion_sort_atraso(atrasados)
            print("\n--- Projetos Atrasados ---")
            for p, status, atraso in atrasados_ordenados:
                print(f"Projeto: {p.nome} | Status: {status} | Atraso: {atraso} dias")

        elif opcao == '11':
            nomes_responsaveis = []
            for p in projetos:
                if p.data_termino is None:
                    idx_emp = busca_binaria_empregado(empregados, p.func_responsavel)
                    if idx_emp != -1:
                        nomes_responsaveis.append(empregados[idx_emp].nome)
            
            nomes_ordenados = selection_sort_nomes(nomes_responsaveis)
            print("\n--- Empregados que Receberão Bônus ---")
            for n in nomes_ordenados:
                print(n)

        elif opcao == '12':
            sub_op = input("1 - Inserir e-mail | 2 - Listar todos: ")
            if sub_op == '1':
                email = input("E-mail do gerente: ")
                hash_emails.inserir(email)
                print("E-mail salvo!")
            elif sub_op == '2':
                hash_emails.imprimir_todos()
                
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()