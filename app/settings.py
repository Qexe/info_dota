import logging


py_logger = logging.getLogger(__name__)
py_logger.setLevel(logging.INFO)

# настройка обработчика и форматировщика в соответствии с нашими нуждами
py_formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
                                                                        # TODO: Разобраться почему не пишутся в файл
py_handler = logging.FileHandler("../main.log", mode='w')
console_out = logging.StreamHandler()

# добавление форматировщика к обработчику
console_out.setFormatter(py_formatter)
py_handler.setFormatter(py_formatter)

# добавление обработчика к логгеру
py_logger.addHandler(py_handler)
py_logger.addHandler(console_out)
