@echo off
echo ============================================
echo        TESTES COMPARATIVOS SAGA
echo ============================================

echo.
echo Verificando se os servicos estao rodando...
curl -s http://localhost:3000/actuator/health > nul
if %errorlevel% neq 0 (
    echo ERRO: Servicos nao estao rodando!
    echo Execute 'docker-compose up' antes de executar os testes.
    pause
    exit /b 1
)

echo Servicos OK!
echo.

echo ============================================
echo           SAGA ORQUESTRADO
echo ============================================
python load-test.py --pattern orchestrated --requests 30 --threads 3

echo.
echo Aguardando 10 segundos...
timeout /t 10 /nobreak > nul

echo ============================================
echo           SAGA COREOGRAFADO
echo ============================================
python load-test.py --pattern choreography --requests 30 --threads 3

echo.
echo ============================================
echo           COMPARATIVO RAPIDO
echo ============================================

echo.
echo Teste rapido - Orquestrado:
curl -s -X POST "http://localhost:3000/api/test/load-test?requests=10" | python -m json.tool

echo.
echo Teste rapido - Coreografado:
curl -s -X POST "http://localhost:3000/api/test/load-test?requests=10" | python -m json.tool

echo.
echo ============================================
echo              METRICAS SISTEMA
echo ============================================

echo.
echo Metricas Order Service:
curl -s "http://localhost:3000/api/test/metrics" | python -m json.tool

echo.
echo Testes concluidos! Verifique os arquivos test_results_*.json
pause