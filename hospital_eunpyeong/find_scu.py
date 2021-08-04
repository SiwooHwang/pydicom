from pydicom.dataset import Dataset
from pynetdicom.pdu_primitives import UserIdentityNegotiation

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind

debug_logger()

# Initialise the Application Entity
ae = AE()
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)
ae.ae_title = 'VIEWREX'

ds = Dataset()
ds.QueryRetrieveLevel = 'SERIES'
# # Unique key for PATIENT level
ds.PatientID = '77089'
ds.PatientName = ''
ds.StudyInstanceUID = '1.3.46.670589.33.1.63749935183101575600001.4639875344515440376'
ds.StudyDescription = ''
ds.SeriesInstanceUID = '1.3.46.670589.33.1.63749935411615645900001.5359564292683842898'
ds.SeriesDescription = ''
ds.instanceNumber = ''

userIdentity = UserIdentityNegotiation()
userIdentity.user_identity_type = 2
userIdentity.primary_field = b'test'
userIdentity.secondary_field = b'1'
negotationItem = []
negotationItem.append(userIdentity)
# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate('192.168.1.240', 108)
if assoc.is_established:
    print('here')
    # Send the C-FIND request
    responses = assoc.send_c_find(
        ds, PatientRootQueryRetrieveInformationModelFind)
    for (status, identifier) in responses:
        if status:
            print('C-FIND query status: 0x{0:04X}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print('Association rejected, aborted or never connected')
