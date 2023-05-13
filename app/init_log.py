import logging as log


log.basicConfig(level=log.INFO, filename="./Files/log/server_log.log", filemode="a",
                format="%(asctime)s %(levelname)s %(message)s")

log.info("___---------- NEW START SERVER ----------___")
