import os
import time
import logging

from pprint import pprint as print
from .manager import Manager
from .manager import Creator as ManagedCreator
from .creator.creator_module import Creator

# If you change __path__, you can force the interpreter to look in a different directory for modules belonging to that package

os.makedirs(os.path.abspath(os.curdir) + os.sep + "logs", exist_ok=True)
logging.basicConfig(level=logging.DEBUG, format=u"%(filename)s[LINE:%(lineno)d]# %(levelname)-8s"
                                                u" [%(asctime)s]  %(message)s",
                    filename=os.path.abspath(os.curdir) + os.sep + "logs" + os.sep + "{}.txt".format(
                        time.strftime('%Y_%b_%d_%H_%M_%S')))

logging.info('Start of program')

#
# def print(*args):
#     for arg in args:
#         pprint(arg)
#         logging.info(args)
