
import xled
from requests.compat import urljoin

testcontroller = xled.ControlInterface('192.168.3.218', '98:f4:ab:36:ae:39')
testcontroller.set_mode('movie')