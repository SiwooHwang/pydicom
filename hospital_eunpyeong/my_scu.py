
from pynetdicom import AE, debug_logger
from pynetdicom.pdu_primitives import UserIdentityNegotiation
debug_logger()

ae = AE()
ae.ae_title = 'VIEWREX2'
userIdentity = UserIdentityNegotiation()
userIdentity.user_identity_type = 2
userIdentity.primary_field = b'test'
userIdentity.second_field = b'1'
negotationItem = []
negotationItem.append(userIdentity)

ae.add_requested_context("1.2.840.10008.1.1")

assoc = ae.associate('192.168.1.240', 108)
if assoc.is_established:
    status = assoc.send_c_echo()
    print('Association established with Echo SCP!')
    assoc.release()
else:
    # Association rejected, aborted or never connected
    print('Failed to associate')
