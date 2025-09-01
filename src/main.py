from ec2_manager import EC2Manager


def main_menu():
    print("\n=== Gerenciador EC2 ===")
    print("1 - Listar instâncias")
    print("2 - Criar instância")
    print("3 - Remover instância")
    print("0 - Sair")
    return input("Escolha uma opção: ")


def instance_menu(instance_id, manager):
    while True:
        info = manager.get_instance(instance_id)
        print(
            f"\nInstância {instance_id} - Estado: {info['state']}, Tipo: {info['type']}, IP: {info['public_ip']}"
        )
        print("1 - Iniciar instância")
        print("2 - Parar instância")
        print("0 - Voltar")
        choice = input("Escolha uma opção: ")
        if choice == "1":
            manager.start_instance(instance_id)
        elif choice == "2":
            manager.stop_instance(instance_id)
        elif choice == "0":
            break
        else:
            print("Opção inválida!")


def main():
    manager = EC2Manager()

    while True:
        choice = main_menu()

        if choice == "1":
            instances = manager.list_instances()
            if not instances:
                print("Nenhuma instância encontrada.")
                continue
            print("\nInstâncias disponíveis:")
            for idx, inst in enumerate(instances):
                print(
                    f"{idx + 1} - ID: {inst['id']} | Estado: {inst['state']} | Tipo: {inst['type']} | IP: {inst['public_ip']}"
                )
            sel = input("Escolha uma instância para gerenciar (ou 0 para voltar): ")
            if sel.isdigit() and int(sel) > 0 and int(sel) <= len(instances):
                instance_menu(instances[int(sel) - 1]["id"], manager)

        elif choice == "2":
            instance_id = manager.create_instance()
            print(f"Instância criada: {instance_id}")

        elif choice == "3":
            inst_id = input("Digite o ID da instância a remover: ")
            manager.terminate_instance(inst_id)

        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
