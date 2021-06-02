# -*- coding: utf-8 -*-

from MainSWU import main
import os
from Utils.DataContainer import instance as DataContainer
# Run my script
if __name__ == '__main__':
    DataContainer.__currentPath__ = os.path.dirname(
        os.path.realpath(__file__))
    DataContainer.__detectorsFile__ = DataContainer.__currentPath__+'/detectors.json'
    DataContainer.__settingsFile__ = DataContainer.__currentPath__+'/settings.json'
    main()
