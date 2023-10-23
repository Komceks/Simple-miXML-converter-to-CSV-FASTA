namespace = {
    'xs': 'http://www.w3.org/2001/XMLSchema',
    'mif': 'http://psi.hupo.org/mi/mif300'
}
# ------------------------------------------------------------------------------
class Interactor:

	
	def __init__(self, interactor):
		self.interactor = interactor
		self.id = self.getInteractorId(interactor)
		self.name, self.aliasDict = self.getNameNalias(interactor)
		self.pxref, self.sxref = self.getXref(interactor)
		self.mType = self.getType(interactor)
		self.organism = self.getOrganism(interactor)
		self.sequence = self.getSequence(interactor)
		self.attribute = self.getAttribute(interactor)


	@staticmethod	
	def getInteractorId(interactor):
		return interactor.get('id', 'N/A')

	@staticmethod
	def getNameNalias(interactor):
		aliasDict = {}

		molecule = interactor.find('.//mif:names/mif:alias[@typeAc="MI:0301"]',
		 namespaces=namespace)

		for alias in interactor.findall('./mif:names/mif:alias',
		 namespaces=namespace):
				
			aliasDict[alias.attrib.get('type', 'N/A')] = alias.text

		if molecule is None:
			molecule = interactor.find('.//mif:names/mif:shortLabel',
		 		namespaces=namespace)
			return molecule.text, aliasDict

		return molecule.text, aliasDict

	@staticmethod
	def getXref(interactor):
		primaryList = []
		secondaryList = []

		xref = interactor.find('.//mif:xref',namespaces=namespace)

		primaryRef = xref.find('./mif:primaryRef',namespaces=namespace)

		secondaryRef = xref.find('./mif:secondaryRef[@db="intact"]',
			namespaces=namespace)	
		if primaryRef is None:
			pref = 'N/A'
		else:
			pref = primaryRef.attrib.get('id', "N/A")
		if secondaryRef is None:
			sref = 'N/A'
		else:
			sref = secondaryRef.attrib.get('id', "N/A")
		return pref, sref

	@staticmethod
	def getType(interactor):
		
		interactorType = interactor.find('./mif:interactorType/mif:names/'
			+ 'mif:shortLabel', namespaces=namespace)
		return interactorType.text

	@staticmethod
	def getOrganism(interactor):
		organism = interactor.find('./mif:organism/mif:names/mif:fullName',
		 namespaces=namespace)
		return organism.text

	@staticmethod
	def getSequence(interactor):
		sequence = interactor.find('./mif:sequence', namespaces=namespace)
		if sequence is not None:
			return sequence.text
		else:
			return "N/A"

	@staticmethod
	def getAttribute(interactor):
		attribute = interactor.find('./mif:atributeList/mif:attribute',
		 namespaces=namespace)
		if attribute is not None:
			return attribute.text
		else:
			return "N/A"

# ------------------------------------------------------------------------------
class Source:

	def __init__(self, source):
		self.source = source
		self.date = self.getSourceDate(source)
		self.name = self.getName(source)
		self.sxref = self.getXref(source)
		self.attribute = self.getAttribute(source)


	@staticmethod	
	def getSourceDate(source):
		return source.get('releaseDate', 'N/A')

	@staticmethod
	def getName(source):
		name = source.find('.//mif:names/mif:fullName',namespaces=namespace)
		
		if name is not None:
			return name.text
		else:
			return "N/A"

	@staticmethod
	def getXref(source):

		xref = source.find('.//mif:xref',namespaces=namespace)

		secondaryRef = xref.find('./mif:secondaryRef[@db="intact"]',
			namespaces=namespace)	
		if secondaryRef is not None:
			return secondaryRef.attrib.get('id', "N/A")
		else:
			return "N/A"

	@staticmethod
	def getAttribute(source):

		attribute = source.find('./mif:atributeList/mif:attribute[@name="url"]',
		 namespaces=namespace)
		if attribute is not None:
			return attribute.text
		else:
			return "N/A"

# ------------------------------------------------------------------------------
class ExperimentDescription:

	def __init__(self, experiment):
		self.experiment = experiment
		self.id = self.getExperimentId(experiment)
		self.name = self.getName(experiment)
		self.pxref, self.sxref = self.getXref(experiment)
		self.host = self.getHost(experiment)
		self.detectMethod = self.getDetectMet(experiment)
		self.participantIdentificationMethod = self.getParticipantIdMet(experiment)
		self.attributes = self.getAttribute(experiment)


	@staticmethod	
	def getExperimentId(experiment):
		return experiment.get('id', 'N/A')

	@staticmethod
	def getName(experiment):
		name = experiment.find('.//mif:names/mif:fullName',namespaces=namespace)
		
		if name is not None:
			return name.text
		else:
			return "N/A"

	@staticmethod
	def getXref(experiment):

		xref = experiment.find('./mif:bibref/mif:xref',namespaces=namespace)
		if xref is None:
			pref = "N/A"
			sref = "N/A"
		else:
			primaryRef = xref.find('./mif:primaryRef',namespaces=namespace)
			
			secondaryRef = xref.find('./mif:secondaryRef[@db="intact"]',
				namespaces=namespace)
			if primaryRef is not None:
				pref = primaryRef.attrib.get('id', "N/A")
			else:
				pref = "N/A"
			
			if secondaryRef is not None:
				sref = secondaryRef.attrib.get('id', "N/A")
			else:
				sref = "N/A"
		
		return pref,sref

	@staticmethod
	def getHost(experiment):
		host = experiment.find('.//mif:hostOrganismList/mif:hostOrganism/' +
			'mif:names/mif:fullName', namespaces=namespace)
		if host is None:
			return 'N/A'
		else:
			return host.text

	@staticmethod
	def getDetectMet(experiment):
		detectMet = experiment.find('./mif:interactionDetectionMethod/' 
			+ 'mif:names/mif:shortLabel', namespaces=namespace)
		if detectMet is not None:
			return detectMet.text
		else:
			return "N/A"

	@staticmethod
	def getParticipantIdMet(experiment):
		participantMet = experiment.find(
			'.//mif:participantIdentificationMethod/mif:names/mif:fullName',
			 namespaces=namespace)
		if participantMet is not None:
			return participantMet.text
		else:
			return "N/A"

	@staticmethod
	def getAttribute(experiment):
		attributes = []
		for attr in experiment.findall('./mif:atributeList/mif:attribute',
		 namespaces=namespace):

			if attribute is not None:
				attributes.append(attribute.text) 
			else:
				attributes.append("N/A")
		return attributes

# ------------------------------------------------------------------------------
class Interaction:  
	
	def __init__(self, interaction):
		self.interaction = interaction
		self.id = self.getExperimentId(interaction)
		self.name = self.getName(interaction)
		self.xref = self.getXref(interaction)
		self.expRef = self.getExperimentRef(interaction)
		self.refDict = self.getParticipantRef(interaction)
		self.host = self.getHost(interaction)
		self.interType = self.getInteractionType(interaction)
		self.attributes = self.getAttributes(interaction)

	@staticmethod	
	def getExperimentId(interaction):
		return interaction.get('id', 'N/A')

	@staticmethod
	def getName(interaction):
		name = interaction.find('.//mif:names/mif:shortLabel',
			namespaces=namespace)
		
		if name is not None:
			return name.text
		else:
			return "N/A"
	
	@staticmethod
	def getXref(interaction):

		xref = interaction.find('./mif:xref',namespaces=namespace)

		secondaryRef = xref.find('./mif:secondaryRef[@db="intact"]',
			namespaces=namespace)
		if secondaryRef is not None:
			return secondaryRef.attrib.get('id', "N/A")
		else:
			return "N/A"
		

	@staticmethod
	def getExperimentRef(interaction):

		ref = interaction.find('./mif:experimentList/mif:experimentRef',
			namespaces=namespace)

		return ref.text

	@staticmethod
	def getParticipantRef(interaction):
		refDict = {}
		it = 0
		stoi = None
		refs = interaction.findall('./mif:participantList/mif:participant/mif:interactorRef',
			namespaces=namespace)
		bioRoles = interaction.findall('./mif:participantList/mif:participant/mif'+
		':biologicalRole/mif:names/mif:fullName',
			namespaces=namespace)
		expRoles = interaction.findall('./mif:participantList/mif:participant/mif'+
			':experimentalRoleList/mif:experimentalRole/mif:names/mif:fullName',
				namespaces=namespace)
			
		for ref in refs:
			participants = interaction.findall('./mif:participantList/mif:participant',
			namespaces=namespace)
			for participant in participants:
				check = participant.find('./mif:interactorRef', namespaces=namespace)
				if check is not None and ref is not None:
					if check.text == ref.text:
						stoi = participant.find('./mif:stoichiometry', namespaces=namespace)
						break
			
			if stoi is not None:
				stoichiometry = stoi.attrib.get('value', 'N/A')
			else:
				stoichiometry = 'N/A'
			refDict[ref.text] = (expRoles[it].text, bioRoles[it].text, stoichiometry)
			it+=1
		return refDict

	@staticmethod
	def getHost(interaction):
		host = interaction.find('./mif:participantList/mif:participant/mif:hostOrganismList/mif:hostOrganism/mif:names/mif:shortLabel',
			namespaces=namespace)
		if host is not None:
			return host.attrib.get('value', 'N/A')
		else:
			return 'N/A'

	@staticmethod
	def getInteractionType(interaction):

		iType = interaction.find('./mif:interactionType/mif:names/mif:fullName',
			namespaces=namespace)
		return iType.text

	@staticmethod
	def getAttributes(interaction):
		attributes = []
		for attr in interaction.findall('./mif:atributeList/mif:attribute',
		 namespaces=namespace):

			if attr is not None:
				attributes.append(attr.text) 
			else:
				attributes.append("N/A")
		return attributes

# ------------------------------------------------------------------------------