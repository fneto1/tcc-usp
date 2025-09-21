# ÍNDICE DE ARQUIVOS - TESTE FINAL REALIZADO

## 📁 ARQUIVOS PRINCIPAIS DO TESTE

### **🧪 Scripts de Teste e Simulação**
- **`academic_test_suite_real_network.py`** - Suite principal de testes com simulação de rede real
- **`chaos_real.py`** - Implementação de chaos engineering real (não simulado)
- **`network_simulator.py`** - Simulador de condições WAN realísticas
- **`statistical_analysis_optimized.py`** - Análise estatística comparativa

### **📊 Dados dos Testes Executados**
- **`academic_results_orchestrated_real_network.json`** (1.16MB) - Resultados completos do padrão Orquestrado
- **`academic_results_choreographed_real_network.json`** (1.16MB) - Resultados completos do padrão Coreografado

### **📈 Análise e Visualizações**
- **`optimized_statistical_analysis_20250921_171830.png`** - Gráficos comparativos das métricas
- **`COMPARACAO_PADROES_SAGA_FINAL.md`** - Análise comparativa detalhada dos padrões
- **`DESCRICAO_COMPLETA_TESTE_REALIZADO.md`** - Documentação completa da metodologia

### **📚 Documentação Acadêmica**
- **`ARTIGO_CIENTIFICO_PADROES_SAGA.txt`** - Artigo científico em formato acadêmico
- **`README.md`** - Documentação geral do projeto
- **`requirements.txt`** - Dependências Python necessárias

## 🔧 COMO EXECUTAR O TESTE

### **Pré-requisitos:**
```bash
pip install -r requirements.txt
```

### **Executar teste Orquestrado:**
```bash
python academic_test_suite_real_network.py orchestrated http://localhost:3000
```

### **Executar teste Coreografado:**
```bash
python academic_test_suite_real_network.py choreographed http://localhost:3000
```

### **Análise Estatística:**
```bash
python statistical_analysis_optimized.py academic_results_orchestrated_real_network.json academic_results_choreographed_real_network.json
```

## 📂 ARQUIVOS ARQUIVADOS

### **`archived_files/`** - Contém versões anteriores e arquivos experimentais:
- Testes de 48h originais
- Tentativas com Toxiproxy
- Análises estatísticas preliminares
- Scripts experimentais diversos

### **`backup-old-tests/`** - Backup dos primeiros testes em localhost

### **`results/`** - Resultados intermediários (pode estar vazio)

## 🎯 PRINCIPAIS RESULTADOS

### **Equivalência Estatística Comprovada:**
- **Latência**: Orquestrado 250.8ms vs Coreografado 254.7ms (diferença 1.5%, p > 0.05)
- **Throughput**: Orquestrado 54.2 vs Coreografado 54.0 req/s (diferença 0.4%, p > 0.05)
- **Taxa de Sucesso**: Orquestrado 95.5% vs Coreografado 96.3% (diferença 0.8%, p > 0.05)
- **P95 Latência**: Orquestrado 339.1ms vs Coreografado 343.3ms (diferença 1.2%, p > 0.05)

### **Conclusão:**
Ambos os padrões apresentam **performance estatisticamente equivalente** sob condições realísticas de rede. A escolha deve ser baseada em requisitos não-funcionais específicos:

- **Orquestrado**: Para controle centralizado e visibilidade
- **Coreografado**: Para autonomia e eliminação de pontos únicos de falha

## 📝 METADADOS DO TESTE

- **Data de Execução**: 21 de Setembro de 2025
- **Duração Total**: ~6 horas
- **Volume de Dados**: 80 medições, ~160.000 requisições
- **Cenários de Rede**: 5 cenários realísticos (Enterprise LAN, Cloud Datacenter, Remote Office, Mobile Users, Poor Connectivity)
- **Payload**: Transações complexas com produtos SMARTPHONE + NOTEBOOK
- **Análise Estatística**: Mann-Whitney U, Shapiro-Wilk, Cohen's d
- **Significância**: α = 0.05

---

**Este teste fornece evidência científica robusta para o TCC, demonstrando equivalência de performance entre os padrões Saga através de metodologia rigorosa e simulação de condições realísticas.**