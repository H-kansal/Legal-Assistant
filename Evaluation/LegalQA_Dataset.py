EXAMPLES = [
  {
    "inputs": {"query": "What does the BNS say about the punishment for theft?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Punishment for theft under BNS",
      "Applicable_Laws": [
        {"act": "BNS", "provision": "Section 303 BNS (replacing IPC 378/379) - theft and its punishment", "context": "General theft, first and subsequent conviction"}
      ],
      "Legal_Explanation": "Theft is defined and punished under Section 303 BNS. First conviction: imprisonment up to 3 years, fine, or both. Second/subsequent conviction: rigorous imprisonment of 1-5 years plus fine.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Under the BNS, simple theft carries imprisonment up to 3 years and/or fine on first conviction, rising to 1-5 years rigorous imprisonment plus fine for repeat offenders."
    }}
  },
  {
    "inputs": {"query": "Which BNS section corresponds to the old IPC Section 302 on murder?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Mapping of IPC Section 302 (murder) to its BNS equivalent",
      "Applicable_Laws": [
        {"act": "BNS", "provision": "Section 103(1) BNS - punishment for murder (replacing IPC 302)", "context": "General murder"},
        {"act": "BNS", "provision": "Section 103(2) BNS - murder by group of 5+ persons on grounds of race, caste, community, sex, place of birth, language or belief", "context": "Mob lynching"}
      ],
      "Legal_Explanation": "IPC Section 302 is now Section 103(1) BNS, with the punishment unchanged: death or life imprisonment, plus fine. BNS 103(2) adds a new clause specifically for murder by 5 or more persons acting together on listed discriminatory grounds.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "IPC 302 maps to BNS Section 103(1); the punishment (death or life imprisonment plus fine) remains the same, with a new sub-clause 103(2) added for mob-lynching-type murders."
    }}
  },
  {
    "inputs": {"query": "What is the difference between culpable homicide and murder under BNS?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Distinction between culpable homicide and murder under BNS",
      "Applicable_Laws": [
        {"act": "BNS", "provision": "Section 100/101 BNS - culpable homicide (replacing IPC 299)", "context": "Causing death without the elevated intent/knowledge required for murder"},
        {"act": "BNS", "provision": "Section 103 BNS - murder (replacing IPC 300/302)", "context": "Causing death with specific intent or knowledge thresholds, subject to statutory exceptions"}
      ],
      "Legal_Explanation": "Culpable homicide causes death without the specific intent/knowledge thresholds that elevate it to murder. Murder requires intent to cause death, intent to cause bodily injury known to be likely to cause death, or knowledge that the act is so imminently dangerous it must in all probability cause death. All murder is culpable homicide, but not all culpable homicide is murder; the dividing line is the degree of intention/knowledge and statutory exceptions such as sudden fight, grave provocation, or exceeding the right of self-defence.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Murder is a more serious subset of culpable homicide, distinguished by a higher degree of intent or knowledge and the absence of mitigating statutory exceptions."
    }}
  },
  {
    "inputs": {"query": "If two people fight and one dies from a single unintended blow during a sudden quarrel with no premeditation, which BNS provisions could apply and why might charges vary?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Applicable BNS provisions for death caused during a sudden, unpremeditated fight",
      "Applicable_Laws": [
        {"act": "BNS", "provision": "Culpable homicide not amounting to murder (corresponding to old IPC 304, Exception 4 to murder)", "context": "Sudden fight, no premeditation, no undue advantage taken"},
        {"act": "BNS", "provision": "Section 103 BNS - murder", "context": "Would apply instead if premeditation or undue advantage is established"}
      ],
      "Legal_Explanation": "This scenario likely falls under culpable homicide not amounting to murder rather than murder under BNS 103, given the absence of premeditation. Charges could vary based on whether there was premeditation, whether undue advantage was taken, whether a dangerous weapon was used, and who struck the first blow. Courts examine intent/knowledge at the time of the act, not just the outcome.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "The facts as described point toward culpable homicide not amounting to murder, though the exact charge depends on weapon use, undue advantage, and who initiated the fight."
    }}
  },
  {
    "inputs": {"query": "What is the procedure for filing an FIR?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Procedure for registering a First Information Report (FIR)",
      "Applicable_Laws": [
        {"act": "BNSS", "provision": "Section 173(1) BNSS (replacing CrPC Section 154) - recording of information in cognizable cases", "context": "Mandatory FIR registration for cognizable offences"},
        {"act": "BNSS", "provision": "Section 173(3) BNSS", "context": "Preliminary inquiry exception for offences punishable with 3-7 years imprisonment"}
      ],
      "Legal_Explanation": "Information about a cognizable offence, given orally or electronically, must be reduced to writing, read back to the informant, signed by them, and entered in the station register. FIR registration is mandatory once a cognizable offence is disclosed, and a free copy must be given to the informant. Section 173(3) BNSS carves out an exception: for offences punishable with 3-7 years imprisonment, police may conduct a preliminary inquiry, with superior officer approval, before registering the FIR.",
      "Procedure": "1) Informant gives information orally/electronically. 2) Police reduce it to writing. 3) Statement is read back to informant. 4) Informant signs it. 5) Entry made in station register. 6) Free copy given to informant. (For offences punishable 3-7 years: optional preliminary inquiry with superior officer's approval before registration.)",
      "Evidence": None,
      "Conclusion": "FIR registration is mandatory on disclosure of a cognizable offence under Section 173(1) BNSS, subject to a new preliminary-inquiry exception under Section 173(3) for mid-range offences."
    }}
  },
  {
    "inputs": {"query": "Is Section 154 CrPC still called Section 154 in BNSS, or has it changed?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Whether CrPC Section 154 retains its number under BNSS",
      "Applicable_Laws": [
        {"act": "BNSS", "provision": "Section 173 BNSS (replacing CrPC Section 154)", "context": "FIR registration, renumbered with an added preliminary-inquiry exception"}
      ],
      "Legal_Explanation": "It has changed. FIR registration is now governed by Section 173 BNSS, not Section 154. Section 173(1) BNSS is substantially similar to the old Section 154 CrPC, but Section 173(3) introduces a new preliminary-inquiry exception that did not exist under the CrPC.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "No, the section number has changed: CrPC Section 154 is now Section 173 BNSS, with an added preliminary-inquiry provision not present in the old law."
    }}
  },
  {
    "inputs": {"query": "What is the difference between a cognizable and non-cognizable offence, and what powers does police have in each?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Distinction between cognizable and non-cognizable offences and corresponding police powers",
      "Applicable_Laws": [
        {"act": "BNSS", "provision": "First Schedule, BNSS (formerly CrPC) - classification of offences as cognizable/non-cognizable", "context": "Determines arrest and investigation powers"}
      ],
      "Legal_Explanation": "In a cognizable offence, police can arrest without a warrant and start investigation without the magistrate's permission; these are typically serious offences like murder, rape, and theft. In a non-cognizable offence, police cannot arrest without a warrant and cannot investigate without the magistrate's permission; these are typically less serious offences like simple hurt or defamation. The classification itself is listed in the First Schedule of the BNSS.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Cognizable offences give police independent arrest and investigation power; non-cognizable offences require a warrant and magistrate's permission, reflecting the relative seriousness of the offence."
    }}
  },
  {
    "inputs": {"query": "Under what circumstances can a police officer arrest a person without a warrant?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Grounds for arrest without a warrant",
      "Applicable_Laws": [
        {"act": "BNSS", "provision": "Provision corresponding to old CrPC Section 41 (exact BNSS section number to be verified against source document)", "context": "Lists grounds for warrantless arrest"}
      ],
      "Legal_Explanation": "Grounds typically include: commission of a cognizable offence in the officer's presence; reasonable suspicion of involvement in a cognizable offence; possession of housebreaking tools without lawful excuse; being a proclaimed offender; obstructing police; deserting from the armed forces; or being reasonably suspected of being about to commit a cognizable offence that cannot otherwise be prevented.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Police may arrest without a warrant on several specific grounds tied to cognizable offences, suspicion, or obstruction; the exact renumbered BNSS section should be verified against the loaded source document."
    }}
  },
  {
    "inputs": {"query": "A person is arrested without a warrant for a bailable offence but the police delay producing them before a magistrate beyond 24 hours. What remedies and rights does the arrested person have?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Rights and remedies for unlawful detention beyond 24 hours for a bailable offence",
      "Applicable_Laws": [
        {"act": "Constitution", "provision": "Article 22(2) - production before magistrate within 24 hours of arrest", "context": "Right against arbitrary detention"},
        {"act": "BNSS", "provision": "Provisions governing bail for bailable offences", "context": "Absolute right to bail on furnishing surety"}
      ],
      "Legal_Explanation": "This violates Article 22(2) of the Constitution, which guarantees that no arrested person can be detained beyond 24 hours, excluding travel time, without being produced before a magistrate. The detention becomes illegal/unconstitutional after 24 hours. For a bailable offence, the arrested person has an absolute right to bail, and the police or magistrate must grant it on furnishing bail.",
      "Procedure": "The arrested person, or someone on their behalf, can seek release via a habeas corpus petition before the High Court or Supreme Court. Departmental action and compensation claims against erring officers are also possible remedies recognized in case law.",
      "Evidence": None,
      "Conclusion": "Detention beyond 24 hours without production before a magistrate is unconstitutional under Article 22(2); the arrested person has an absolute right to bail (being a bailable offence) and can seek habeas corpus relief, alongside possible compensation per case law such as the D.K. Basu guidelines."
    }}
  },
  {
    "inputs": {"query": "What changed about the use of electronic/video-conferencing means for trial procedures between CrPC and BNSS?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Changes to electronic/video-conferencing procedures between CrPC and BNSS",
      "Applicable_Laws": [
        {"act": "BNSS", "provision": "Multiple provisions across FIR filing, statement recording, trial conduct, evidence recording, and summons (exact section numbers to be verified against source document)", "context": "Formalization of electronic and audio-video means in criminal procedure"}
      ],
      "Legal_Explanation": "BNSS explicitly expands and formalizes the use of electronic communication and audio-video means for FIR filing, recording statements, conducting trials, evidence recording, and serving summons. This is a deliberate modernization that was not as extensively codified in the CrPC.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "BNSS significantly broadens the legal recognition of electronic and video-conferencing means across multiple stages of criminal procedure compared to the CrPC; exact section numbers should be verified against the loaded BNSS document since this spans several provisions rather than one section."
    }}
  },
  {
    "inputs": {"query": "What is the limitation period for filing a civil suit for recovery of money under a written contract?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Limitation period for a civil suit to recover money under a written contract",
      "Applicable_Laws": [
        {"act": "Limitation Act, 1963", "provision": "Article 1 / Article 14-22 range (depending on specific claim type)", "context": "Limitation period for contractual money claims, generally 3 years from when the right to sue accrues"}
      ],
      "Legal_Explanation": "This falls under the Limitation Act, 1963, not the CPC itself. The general limitation period for contractual money claims is 3 years from when the right to sue accrues. A RAG system answering this purely from a CPC document, without flagging that limitation periods live in a separate Act, would be a scope/honesty failure worth flagging in evaluation.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "The applicable limitation period is generally 3 years under the Limitation Act, 1963, not the CPC; this is outside the scope of a CPC-only knowledge base and should be flagged as such if not separately loaded."
    }}
  },
  {
    "inputs": {"query": "What is the meaning of 'res judicata' under CPC?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Meaning and scope of res judicata under CPC",
      "Applicable_Laws": [
        {"act": "CPC", "provision": "Section 11 CPC - res judicata", "context": "Bar on re-litigating matters already decided"}
      ],
      "Legal_Explanation": "Res judicata, defined under Section 11 CPC, bars a court from trying any suit or issue that has already been directly and substantially decided in a previous suit between the same parties, or parties litigating under the same title, by a competent court, and which has attained finality. Its purpose is to prevent re-litigation of the same matter and ensure finality of judgments.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Res judicata under Section 11 CPC prevents the same parties from re-litigating a matter already finally decided by a competent court."
    }}
  },
  {
    "inputs": {"query": "What is the procedure for obtaining a temporary injunction under CPC, and what must the plaintiff prove?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Procedure and requirements for obtaining a temporary injunction under CPC",
      "Applicable_Laws": [
        {"act": "CPC", "provision": "Order XXXIX, Rules 1 and 2 CPC - temporary injunctions", "context": "Conditions and procedure for granting interim injunctive relief"}
      ],
      "Legal_Explanation": "Governed by Order XXXIX, Rules 1 and 2 CPC, the plaintiff applies to the court, usually with the suit or at any later stage, and must establish three things: a prima facie case, balance of convenience in their favour, and irreparable injury or harm if the injunction is not granted. The court can grant an ex-parte injunction in urgent cases, subject to later confirmation after hearing the other side.",
      "Procedure": "1) Plaintiff files application under Order XXXIX, Rules 1/2, with or after filing the suit. 2) Court examines prima facie case, balance of convenience, and irreparable injury. 3) Court may grant ex-parte interim injunction in urgent cases. 4) Other side is heard before the injunction is confirmed, modified, or vacated.",
      "Evidence": None,
      "Conclusion": "A temporary injunction under CPC requires the plaintiff to prove a prima facie case, balance of convenience, and irreparable injury, with courts empowered to grant urgent ex-parte relief subject to later confirmation."
    }}
  },
  {
    "inputs": {"query": "If a decree is passed in one state and the judgment debtor's assets are in another state, what is the process to execute that decree, and what challenges typically arise?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Process for inter-state execution of a civil decree",
      "Applicable_Laws": [
        {"act": "CPC", "provision": "Section 38-39 CPC - courts by which decrees may be executed / transfer of decree", "context": "Transfer of decree to court where assets/debtor are located"},
        {"act": "CPC", "provision": "Section 42 CPC - powers of court executing transferred decree", "context": "Receiving court executes as if it had passed the decree"},
        {"act": "CPC", "provision": "Section 47 CPC - questions to be determined by the court executing the decree", "context": "Procedural objections raised by judgment debtor at execution stage"}
      ],
      "Legal_Explanation": "The decree-holder applies to the court that passed the decree, under Section 38-39 CPC, to transfer the decree for execution to the court within whose jurisdiction the assets or judgment-debtor are located. The receiving court then executes it as if it had passed the decree itself, under Section 42 CPC. Practical challenges include delays in the transfer process, difficulty tracing or attaching assets across jurisdictions, the judgment debtor concealing or transferring assets, and procedural objections raised at the execution stage under Section 47 CPC.",
      "Procedure": "1) Decree-holder applies to the originating court for transfer of decree (Section 38-39 CPC). 2) Decree is transferred to the court with jurisdiction over the debtor's assets. 3) Receiving court executes the decree (Section 42 CPC). 4) Judgment debtor may raise objections under Section 47 CPC during execution.",
      "Evidence": None,
      "Conclusion": "Inter-state execution requires formal transfer of the decree under Sections 38-39 and 42 CPC to the court with jurisdiction over the debtor's assets, and commonly faces delays, asset-tracing difficulties, and procedural objections under Section 47 CPC."
    }}
  },
  {
    "inputs": {"query": "What does Section 66 of the IT Act deal with?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Scope of Section 66 of the IT Act",
      "Applicable_Laws": [
        {"act": "IT Act", "provision": "Section 66 - computer-related offences", "context": "Punishes dishonest or fraudulent acts referred to in Section 43"},
        {"act": "IT Act", "provision": "Section 43 - referenced acts (unauthorized access, data theft, introducing viruses, damaging computer systems)", "context": "Underlying acts that, if done dishonestly/fraudulently, attract Section 66 punishment"}
      ],
      "Legal_Explanation": "Section 66 deals with computer-related offences, punishing dishonest or fraudulent acts referred to in Section 43, such as unauthorized access, data theft, introducing viruses, and damaging computer systems, with imprisonment up to 3 years, fine up to Rs. 5 lakh, or both.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Section 66 IT Act criminalizes dishonest or fraudulent computer-related acts under Section 43, with punishment of up to 3 years imprisonment and/or fine up to Rs. 5 lakh."
    }}
  },
  {
    "inputs": {"query": "Is Section 66A of the IT Act still valid law?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Current legal validity of Section 66A, IT Act",
      "Applicable_Laws": [
        {"act": "IT Act", "provision": "Section 66A (struck down)", "context": "Previously penalized offensive electronic messages"},
        {"act": "Constitution", "provision": "Article 19(1)(a) and Article 19(2)", "context": "Freedom of speech and permissible reasonable restrictions, basis for striking down Section 66A"}
      ],
      "Legal_Explanation": "No, Section 66A was struck down in its entirety by the Supreme Court in Shreya Singhal v. Union of India (2015) 5 SCC 1, as unconstitutional and violative of Article 19(1)(a), not saved by the reasonable-restrictions exception under Article 19(2). It was declared void ab initio. Despite this, the text still appears in some unupdated copies of the IT Act and continues to be misused in some FIRs, a known real-world problem, but it has no legal force.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Section 66A is not valid law; it was struck down as unconstitutional and void ab initio by the Supreme Court in Shreya Singhal v. Union of India (2015), and any continued reliance on it is legally incorrect."
    }}
  },
  {
    "inputs": {"query": "What are the legal requirements for an electronic record to be admissible as evidence, and how does this connect with the Evidence Act?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Admissibility requirements for electronic records as evidence",
      "Applicable_Laws": [
        {"act": "Evidence Act", "provision": "Section 65B Indian Evidence Act (or BSA equivalent) - admissibility of electronic records", "context": "Certificate requirement for secondary electronic evidence"},
        {"act": "IT Act", "provision": "Sections 4 and 5 IT Act - legal recognition of electronic records and digital signatures", "context": "Underlying recognition that supports admissibility under the Evidence Act"}
      ],
      "Legal_Explanation": "Electronic records are admissible under Section 65B of the Indian Evidence Act, or its BSA equivalent, which requires a certificate identifying the electronic record, describing how it was produced, and certifying the device or computer's particulars, signed by a person in a responsible official position. The Supreme Court in Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) held this certificate is mandatory for secondary electronic evidence, with limited exceptions. This connects to the IT Act's recognition of electronic records and digital signatures as legally valid documents under Sections 4 and 5.",
      "Procedure": "Obtain a Section 65B-compliant certificate identifying the electronic record, describing its mode of production, and certifying the relevant device, signed by a person in a responsible official position in relation to the device.",
      "Evidence": "A Section 65B certificate is the key evidentiary requirement; without it, secondary electronic evidence is generally inadmissible except in limited recognized circumstances.",
      "Conclusion": "Electronic records require a Section 65B certificate to be admissible as secondary evidence, a requirement reinforced as mandatory by the Supreme Court in Arjun Panditrao Khotkar (2020), and this dovetails with the IT Act's recognition of electronic records under Sections 4 and 5."
    }}
  },
  {
    "inputs": {"query": "A company suffers a data breach where customer financial data is leaked due to negligence in maintaining security practices. What liability could the company face under the IT Act, and what compliance obligations might have been missed?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Corporate liability under the IT Act for a negligence-based data breach",
      "Applicable_Laws": [
        {"act": "IT Act", "provision": "Section 43A IT Act - compensation for failure to protect sensitive personal data", "context": "Liability for negligent security practices causing wrongful loss/gain"},
        {"act": "IT Act", "provision": "SPDI Rules, 2011 (framework referenced under Section 43A)", "context": "Reasonable security practices and procedures, e.g. IS/ISO 27001-type standards"}
      ],
      "Legal_Explanation": "Section 43A IT Act makes a body corporate liable to pay compensation to affected persons if it is negligent in implementing and maintaining reasonable security practices and procedures while handling sensitive personal data, causing wrongful loss or wrongful gain. Compliance obligations likely missed include adopting a documented security policy, such as IS/ISO 27001 or an equivalent standard referenced under the SPDI Rules 2011 framework, and following grievance and breach-notification practices. India also now has the Digital Personal Data Protection Act, 2023, which may run alongside or eventually supersede some of this framework.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "The company faces potential compensation liability under Section 43A IT Act for negligent data security practices, and likely failed to maintain SPDI Rules-compliant reasonable security standards; the Digital Personal Data Protection Act, 2023 may also be relevant depending on what the knowledge base covers."
    }}
  },
  {
    "inputs": {"query": "What is the difference between 'relevant facts' and 'facts in issue' under the Indian Evidence Act / BSA?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Distinction between 'relevant facts' and 'facts in issue' under the Evidence Act/BSA",
      "Applicable_Laws": [
        {"act": "Evidence Act", "provision": "Definitions of 'facts in issue' and 'relevant facts'", "context": "Foundational evidentiary concepts"}
      ],
      "Legal_Explanation": "'Facts in issue' are the facts directly disputed by the parties, i.e., what the court must decide to resolve the case. 'Relevant facts' are facts that are not in issue themselves but are connected to a fact in issue in ways recognized by the Act, such as cause and effect, motive, opportunity, or conduct, and therefore help prove or disprove a fact in issue. All facts in issue are relevant, but not all relevant facts are facts in issue.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Facts in issue are the core disputed matters the court must decide, while relevant facts are connected facts that help establish or disprove those matters; the former is a subset of the latter."
    }}
  },
  {
    "inputs": {"query": "What is a dying declaration, and under what conditions is it admissible?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Definition and admissibility conditions for a dying declaration",
      "Applicable_Laws": [
        {"act": "Evidence Act", "provision": "Section 32(1) Evidence Act (traditionally) - statements as to cause of death", "context": "Exception to the hearsay rule"}
      ],
      "Legal_Explanation": "A dying declaration is a statement made by a person as to the cause of their death, or the circumstances of the transaction resulting in their death, made when death is imminent or has since occurred. It is admissible as an exception to the hearsay rule even though the maker cannot be cross-examined, provided the statement relates to the cause or circumstances of death and the person is unavailable to testify, usually because they died. Courts require it to be voluntary and coherent, and ideally recorded or certified by a magistrate or doctor where possible, though that is not a strict legal requirement; a credible, consistent dying declaration alone can sustain a conviction.",
      "Procedure": None,
      "Evidence": "A dying declaration itself functions as a form of evidence; reliability is strengthened where it is recorded/certified by a magistrate or medical professional, though not strictly required.",
      "Conclusion": "A dying declaration is admissible as a statutory exception to hearsay, provided it relates to the cause or circumstances of the deceased's death and is found voluntary and coherent; it can alone sustain a conviction if credible."
    }}
  },
  {
    "inputs": {"query": "If a confession is made by an accused to a police officer while in custody, is it admissible? What if the same confession leads police to recover a weapon?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Admissibility of custodial confessions to police, and the discovery-of-fact exception",
      "Applicable_Laws": [
        {"act": "Evidence Act", "provision": "Section 25 Evidence Act (traditionally) - confession to police officer not admissible", "context": "General bar on police confessions"},
        {"act": "Evidence Act", "provision": "Section 26 Evidence Act (traditionally) - confession while in police custody", "context": "Inadmissible unless made in immediate presence of a magistrate"},
        {"act": "Evidence Act", "provision": "Section 27 Evidence Act (traditionally) - discovery of fact exception", "context": "Information leading to discovery of a fact becomes admissible to that extent"}
      ],
      "Legal_Explanation": "A confession made to a police officer is generally inadmissible, and a confession made while in police custody to anyone is also inadmissible unless made in the immediate presence of a magistrate. However, there is a specific discovery exception: if the confession leads to the discovery of a fact, such as recovery of a weapon, then so much of the information as distinctly relates to that discovered fact becomes admissible, even though the rest of the confession remains inadmissible. So the confession itself stays out, but the discovery-related portion, such as the location of a hidden weapon, can come in.",
      "Procedure": None,
      "Evidence": "The recovered weapon, and the specific statement distinctly relating to its discovery, are admissible; the broader confession of guilt is not.",
      "Conclusion": "The general confession to police is inadmissible, but the portion of the statement that distinctly led to recovery of the weapon is admissible under the discovery-of-fact exception."
    }}
  },
  {
    "inputs": {"query": "What fundamental rights are guaranteed under Article 21 of the Constitution of India?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Scope of rights guaranteed under Article 21 of the Constitution",
      "Applicable_Laws": [
        {"act": "Constitution", "provision": "Article 21 - protection of life and personal liberty", "context": "Core fundamental right, judicially expanded over time"}
      ],
      "Legal_Explanation": "Article 21 guarantees the right to life and personal liberty: no person shall be deprived of life or personal liberty except according to procedure established by law. Through judicial interpretation since Maneka Gandhi v. Union of India (1978), this has been expanded to include the right to live with dignity, right to privacy, right to a clean environment, right to speedy trial, right to legal aid, right to health, and various other rights read into 'life' and 'personal liberty', far beyond mere physical existence.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Article 21 guarantees life and personal liberty, judicially expanded since Maneka Gandhi (1978) to cover dignity, privacy, health, speedy trial, legal aid, and a clean environment, among other derived rights."
    }}
  },
  {
    "inputs": {"query": "What is the difference between fundamental rights and directive principles of state policy, and can the latter be enforced in court?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Distinction between Fundamental Rights and Directive Principles, and enforceability of the latter",
      "Applicable_Laws": [
        {"act": "Constitution", "provision": "Part III, Articles 12-35 - Fundamental Rights", "context": "Justiciable, directly enforceable in court"},
        {"act": "Constitution", "provision": "Part IV, Articles 36-51 - Directive Principles of State Policy", "context": "Non-justiciable policy guidelines"},
        {"act": "Constitution", "provision": "Article 32 and Article 226", "context": "Mechanisms to enforce Fundamental Rights via Supreme Court/High Courts"}
      ],
      "Legal_Explanation": "Fundamental Rights, in Part III, Articles 12-35, are justiciable and directly enforceable in court; citizens can approach the Supreme Court under Article 32 or High Courts under Article 226 if violated. Directive Principles of State Policy, in Part IV, Articles 36-51, are non-justiciable; they are guidelines or goals for the state to aim toward in policymaking for social and economic welfare, but courts cannot directly enforce them or strike down laws solely for failing to implement them. However, courts have increasingly read Directive Principles together with Fundamental Rights, especially Article 21, to give them indirect enforceability in many landmark judgments.",
      "Procedure": None,
      "Evidence": None,
      "Conclusion": "Fundamental Rights are directly enforceable in court, while Directive Principles are not, though courts have increasingly used Article 21 to give Directive Principles indirect enforceability through judicial interpretation."
    }}
  },
  {
    "inputs": {"query": "Under what conditions can fundamental rights be suspended, and how does this interact with the proclamation of emergency under Article 352?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Conditions for suspension of fundamental rights during a national emergency",
      "Applicable_Laws": [
        {"act": "Constitution", "provision": "Article 352 - proclamation of national emergency", "context": "Trigger for emergency-related suspensions"},
        {"act": "Constitution", "provision": "Article 358 - suspension of Article 19 freedoms during emergency", "context": "Automatic suspension limited to war/external aggression grounds, post 44th Amendment"},
        {"act": "Constitution", "provision": "Article 359 - suspension of enforcement of other fundamental rights", "context": "Presidential order required; Articles 20 and 21 cannot be suspended, post 44th Amendment"}
      ],
      "Legal_Explanation": "During a national emergency proclaimed under Article 352, Article 358 automatically suspends Article 19 freedoms, such as speech and assembly, for the duration of the emergency, but only when the emergency is on grounds of war or external aggression, post the 44th Amendment. Article 359 allows the President to suspend the right to enforce other fundamental rights, except Articles 20 and 21 which can never be suspended post the 44th Amendment, by specific order during an emergency. This means courts cannot be approached to enforce the specified suspended rights for that period, a major check that was controversially used during the 1975 Emergency, which led to the 44th Amendment safeguards being added.",
      "Procedure": "Suspension under Article 358 is automatic upon proclamation (for war/external aggression emergencies); suspension under Article 359 requires a specific Presidential order naming the rights suspended.",
      "Evidence": None,
      "Conclusion": "Fundamental rights can be suspended during a proclaimed national emergency via Articles 358 and 359, but Articles 20 and 21 are permanently protected from suspension following the 44th Amendment."
    }}
  },
  {
    "inputs": {"query": "A person is arrested under BNS for cyber fraud involving forged electronic documents. Which provisions across BNS, BNSS, IT Act, and the Evidence Act would typically come into play in investigating and prosecuting this case?"},
    "outputs": {"answer": {
      "Legal_Issue_Identified": "Cross-statute provisions applicable to investigation and prosecution of cyber fraud involving forged electronic documents",
      "Applicable_Laws": [
        {"act": "BNS", "provision": "Cheating/fraud provisions (corresponding to old IPC 420 range)", "context": "Substantive offence of fraud"},
        {"act": "BNS", "provision": "Forgery provisions (corresponding to old IPC 463-471 range)", "context": "Substantive offence of forging documents"},
        {"act": "BNSS", "provision": "Arrest procedure (Section 35 range) for cognizable offences", "context": "Power of arrest without warrant"},
        {"act": "BNSS", "provision": "Section 173 BNSS", "context": "FIR registration"},
        {"act": "BNSS", "provision": "Search/seizure provisions for electronic devices", "context": "Evidence collection from digital devices"},
        {"act": "IT Act", "provision": "Section 66 - computer-related offences/fraud", "context": "Punishes fraudulent acts via computer resource"},
        {"act": "IT Act", "provision": "Section 66C/66D-type provisions - identity theft, cheating by personation using computer resource", "context": "Specific cyber-fraud offences"},
        {"act": "Evidence Act", "provision": "Section 65B-equivalent certificate requirement", "context": "Admissibility of forged electronic documents and digital trail such as emails, logs, metadata"}
      ],
      "Legal_Explanation": "BNS provisions on cheating/fraud and forgery establish the substantive offence. BNSS governs arrest without warrant for cognizable offences, FIR registration, and search/seizure of electronic devices and statements. The IT Act's Section 66 and identity-theft/personation provisions address the cyber-specific fraud elements. The Evidence Act's Section 65B-equivalent certificate requirement is needed to make the forged electronic documents and any digital trail, such as emails, logs, or metadata, admissible in court. Exact section numbers for BNS forgery/cheating provisions and IT Act 66C/66D-type sections should be verified against the loaded source documents.",
      "Procedure": "1) FIR registered under BNSS Section 173. 2) Arrest without warrant under BNSS arrest provisions for the cognizable cyber-fraud offence. 3) Search and seizure of electronic devices per BNSS provisions. 4) Investigation invokes BNS cheating/forgery provisions alongside IT Act Section 66/66C/66D-type provisions. 5) Digital evidence, such as forged documents, emails, and logs, is authenticated via a Section 65B-equivalent certificate for admissibility at trial.",
      "Evidence": "Forged electronic documents and supporting digital trail (emails, server logs, metadata) require a Section 65B-equivalent certificate to be admissible.",
      "Conclusion": "Prosecuting this case requires synthesizing BNS fraud/forgery provisions, BNSS arrest/FIR/search procedures, IT Act cyber-fraud provisions, and an Evidence Act Section 65B-equivalent certificate to admit the digital evidence; exact section numbers should be confirmed against the loaded documents."
    }}
  }
]