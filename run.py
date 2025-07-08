
#!/usr/bin/env python3
"""
Script principal para processamento de horários XML
"""

import sys
import os
import argparse
from datetime import datetime

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from processor import ScheduleProcessor
from utils import setup_logging

def main():
    parser = argparse.ArgumentParser(description="Processador de Horários XML")
    parser.add_argument('--force', action='store_true', 
                       help='Força processamento mesmo sem alterações na fonte')
    parser.add_argument('--config', default='config/channel-offsets.json',
                       help='Caminho para arquivo de configuração')
    parser.add_argument('--log-level', default='INFO',
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Nível de log')
    parser.add_argument('--log-file', 
                       help='Arquivo de log (opcional)')
    
    args = parser.parse_args()
    
    # Configurar logging
    if not args.log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.log_file = f"logs/processing_{timestamp}.log"
    
    setup_logging(args.log_level, args.log_file)
    
    try:
        # Criar e executar processador
        processor = ScheduleProcessor(config_path=args.config)
        success = processor.run(force_download=args.force)
        
        if success:
            print("✅ Processamento concluído com sucesso!")
            print("📁 Arquivo principal: adjusted_schedule.xml.gz")
            sys.exit(0)
        else:
            print("ℹ️  Nenhum processamento necessário")
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Erro no processamento: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
