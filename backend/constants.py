from enum import Enum

class TextEnum(Enum):
    @classmethod
    def names(cls):
        return tuple(e.name for e in cls)

    @classmethod
    def choices(cls):
        return[(e.name, e.value) for e in cls]

class EncounterClass(TextEnum):
    AMB = 'Outpatient'
    IMP = 'Inpatient'
    
class EncounterStatus(TextEnum):
    PLANNED = 'Planned'
    ARRIVED = 'Arrived'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'
    CANCELLED = 'Cancelled'

class DiagnosisRole(TextEnum):
    AD = 'Admission'
    DD = 'Discharge'
    PRE_OP = 'Pre-operation'
    POST_OP = 'Post-operation'

class ConditionSeverity(TextEnum):
    SEVERE = 'Severe'
    MODERATE = 'Moderate'
    MILD = 'Mild'

class ObservationValueType(TextEnum):
    QUANTITY = 'Quantity'
    TEXT = 'Text'
    CODE = 'Code'
    DATETIME = 'DateTime'

class Permissions(TextEnum):
    ADD_DEPARTMENT = 'Add Department'
    CHANGE_DEPARTMENT = 'Change Department'
    DELETE_DEPARTMENT = 'Delete Department'
    VIEW_DEPARTMENT = 'View Department'