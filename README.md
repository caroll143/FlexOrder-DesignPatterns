# FlexOrder-DesignPatterns
A arquitetura do sistema segue o paradigma orientado a objetos e adota os padrões Strategy, Decorator e Facade para estruturar o processo de checkout de forma modular e flexível. Os pagamentos e fretes são tratados como estratégias intercambiáveis, permitindo variar o comportamento conforme o contexto. Já os descontos e taxas adicionais são aplicados por meio de decoradores, que estendem as funcionalidades sem modificar o código existente. Por fim, o CheckoutFacade atua como ponto central do processo, coordenando o cálculo de valores, o processamento do pagamento e a emissão da nota fiscal.
Criar o calculador principal e aplicar os decorators de desconto conforme as regras definidas.
Determinar o valor total com os descontos aplicados.
Calcular o frete utilizando a estratégia apropriada.
Adicionar o decorator de embalagem, caso seja necessário.
Obter o valor final somando o total (com descontos e possíveis taxas) ao frete.
Executar o processamento do pagamento através da estratégia correspondente.
Integrar e coordenar todos os subsistemas após a confirmação bem-sucedida do pagamento.