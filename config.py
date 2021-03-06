# encoding: utf8
from dosutil import ANSI, ANSI2OEM
import parse

import time, os
import ConfigParser
from datetime import datetime
from utils import Proxy, formatLabel
import codecs

try:
    with open("SelectMP.ini.encoding") as f:
        iniEncoding = f.read().strip()
except IOError as err:
    print "Could not readfind \"SelectMP.ini.encoding\", using default \"utf8\""
    iniEncoding = "utf8"
else:
    print "Encoding found:%s"%iniEncoding

class IniParser(ConfigParser.ConfigParser):
    def __init__(self, ini_path="SelectMP.ini"):
        ConfigParser.ConfigParser.__init__(self)
        #os.path.splitext(__file__)[0] +'.ini'
        try:
            with codecs.open(ini_path, 'r', iniEncoding) as f:
                self.readfp(f)
        except IOError as err:
            print("\n\n Cannot read (%s): \n %s.\n check your config file.\n Exiting" % (ini_path, str(err)))
            sys.exit(1)

        self._export                        = Proxy()
        self._export.path                   = self.get("_export", 'path')
        self._export.data                   = self.get("_export", 'data')

        self._import                        = Proxy()
        self._import.path                   = self.get("_import", 'path')
        # self.paths._exportDataDir         = os.path.join(self._export.path, self._export.path)

        # self.files                          = Proxy()
        # self.files.products                 = self.get("SelectMP", 'art_id_file')

        
        # self.files.contractors              = self.get("SelectMP", 'contr_id_file')
        # self.files.dolphine_dealers_file    = os.path.join(self._import.path, self.get("SelectMP", 'dealers'))
        # self.files.file_dost                = self.get("SelectMP", 'file_dost') #'dost_MP.PRN'
        # self.files.file_prod                = self.get("SelectMP", 'file_prod') #'prod_MP.PRN'

        # self.files.export                   = Proxy()
        # self.files.export.artikuli          = os.path.join(self._export.path, 'artikuli-new.txt')
        # self.files.export.kontragenti       = os.path.join(self._export.path, 'contragenti-new.txt')

        self.encoding = Proxy()
        self.encoding._import               = self.get("_import", "encoding")
        self.encoding._export               = self.get("_export", "encoding")

        self.saldo = Proxy(data={"encoding":self.encoding})
        self.saldo.do                       = self.get("saldo", "do")
        self.saldo.yy                       = self.get("saldo", "YearYY")
        self.saldo._import                  = os.path.join(self._import.path, self.get("saldo", "import_file"))
        self.saldo._export                  = os.path.join(self._export.path, self.get("saldo", "replic"))
        self.saldo.skips                    = self.get("saldo", "skips")
        self.errors                         = Proxy()
        self.errors.missingEIK              = "Липсва ЕИК към %s № (%s) от дата:%s; "
        self.errors.timeStamp               = "\n\n!!! Date & time: %s\n"%(datetime.now())
        if __debug__:
            formatLabel("CONFIG")
            print "skips:\n%s" % self.saldo.skips.encode("cp1251")
            formatLabel("CONFIG", end=True)
