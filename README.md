# Event Sourcing Implementation

## Configuração

Adicionar as configurações necessárias aos settings da aplicação:

```python
    INSTALLED_APPS += ('events_manager.event_sourcing',)
```

Para receber logs de erros deve adicionar o logger 'events_manager' ao logs do django