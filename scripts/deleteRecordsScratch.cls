List<String> objSet8 = new List<String>{
    'TempoBloqueioVenda__c',
    'IntervaloVisita__c',
    'QuantidadeSemanasCiclo__c',
    'Banco__c',
    'CicloVisita__c',
    'EmailRevisaoCredito__c',
    'AdmVendasProfileName__c',
    'SLAIntegracao__c',
    'SimulacaoPedidos__c',
    'ProdutoPricing__c',
    'GrupoClientePricing__c',
    'CanalVendas__c',
    'TipoProdutoPricing__c',
    'DescontoAcertoPreco__c',
    'Pais__c',
    'Estado__c',
    'Microrregiao__c',
    'Regiao2__c',
    'Regiao1__c',
    'Estabelecimento__c',
    'VersaoProdutoPricing__c',
    'Frete__c',
    'MarcaProdutoPricing__c'
};
List<String> objSet7 = new List<String>{
    'CondicaoPagamento__c',
    'Comissao__c',
    'DescontoBandaPricing__c',
    'FreteTransferencia__c',
    'FreteSaida__c',
    'Representante__c',
    'ExcecaoClienteProduto__c',
    'Cidade__c',
    'HierarquiaDeProduto__c'
};
List<String> objSet6 = new List<String>{
    'Product2',
    'Cota__c',
    'ItemExcecaoCliente__c',
    'DescontoBanda__c'
};
List<String> objSet5 = new List<String>{
    'LeadTime__c'
};
List<String> objSet4 = new List<String>{
    'Matriz__c',
    'Bandeira__c',
    'Account',
    'CondicaoCliente__c',
    'Endereco__c',
    'ParametroPedidoMae__c'
};
List<String> objSet3 = new List<String>{
    'ProdutoFilialFaturamento__c',
    'CustoProducao__c'
};
List<String> objSet2 = new List<String>{
    'PosicionamentoProduto__c',
    'FaixaPreco__c'
};
List<String> objSet1 = new List<String>{
    'Margem__c',
    'Impostos__c'
};
List<String> objSet0 = new List<String>{
    'MapaDistribuicao__c'
};

for(integer i = objSet.size()-1; i>=0;i--){
    delete Database.query('SELECT id FROM '+objSet[i]);
}