# -- Server --
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 8080
ROUTE_PORT_MAPPING = {
    8001: '/radare1/',
    8002: '/radare2/',
    8003: '/radare3/',
    8004: '/radare4/',
}

#  -- Scheduler --
RADARE_TIMEOUT = 120
RADARE_PORTS = list(ROUTE_PORT_MAPPING.keys())
QUEUE_BLOCK_TIMEOUT = 1
