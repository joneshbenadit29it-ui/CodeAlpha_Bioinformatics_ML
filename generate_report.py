import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Dynamically calculates total pages and adds a professional running header and footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4A5568"))
        
        # Draw top running header (Skip on page 1 for title aesthetics)
        if self._pageNumber > 1:
            self.drawString(54, 750, "CodeAlpha Mini-Project: ML in Bioinformatics")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Draw bottom footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "Confidential - Academic & Research Internship Report")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 52, 558, 52)
        
        self.restoreState()

def build_pdf(filename="CodeAlpha_Bioinformatics_ML.pdf"):
    # Target 0.75 in margins to allow thorough 5-6 page textual layout
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette Style Definition
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1E3A8A"),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#475569"),
        spaceAfter=25
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#0D9488"),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#334155"),
        spaceAfter=12,
        alignment=4 # Justified
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=20,
        firstLineIndent=-10,
        spaceAfter=6
    )

    story = []

    # ==========================================
    # TITLE SECTION & METADATA
    # ==========================================
    story.append(Paragraph("Applications of Machine Learning in Bioinformatics", title_style))
    story.append(Paragraph("<b>Domain:</b> Bioinformatics Task Report<br/><b>Prepared for:</b> CodeAlpha Internship Program<br/><b>Status:</b> Completed Project Report", subtitle_style))
    story.append(Spacer(1, 15))
    
    # Decorative horizontal block
    meta_table = Table([[ "" ]], colWidths=[504], rowHeights=[4])
    meta_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1E3A8A"))]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # ==========================================
    # PAGE 1: EXECUTIVE SUMMARY & INTRODUCTION
    # ==========================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "This mini-project report explores the revolutionary integration of Machine Learning (ML) techniques within the domain of bioinformatics. As high-throughput sequencing technologies scale exponentially, biological data production has far outpaced traditional analysis methods. This study examines how deep learning, support vector machines, and ensemble models convert raw, high-dimensional biomolecular data into actionable clinical insights. We systematically analyze applications across structural bioinformatics, functional genomics, and personalized drug design.", 
        body_style
    ))
    
    story.append(Paragraph("2. Introduction to Bioinformatics in the Omics Era", h1_style))
    story.append(Paragraph(
        "The contemporary biological sciences have fundamentally transformed into data-driven disciplines. The advent of Next-Generation Sequencing (NGS) allows laboratories to map an entire human genome in hours, generating terabytes of raw sequence strings. Bioinformatics serves as the critical bridge transforming this numerical and textual landscape into physiological comprehension.", 
        body_style
    ))
    story.append(Paragraph(
        "Historically, algorithmic approaches in bioinformatics relied heavily on deterministic, heuristic-driven computational models (e.g., standard dynamic programming for sequence alignments). While highly rigorous, these strategies break down when confronted with multi-omic datasets displaying intricate, non-linear biological interactions. Machine learning offers a paradigm shift by learning complex operational features directly from raw observational data without explicit semantic modeling.", 
        body_style
    ))
    
    story.append(PageBreak()) # Shift to Page 2

    # ==========================================
    # PAGE 2: GENOMICS & SEQUENCE ANALYSIS
    # ==========================================
    story.append(Paragraph("3. Core Applications in Functional Genomics", h1_style))
    story.append(Paragraph(
        "Functional genomics seeks to understand the operational characteristics of genomic sequences. Machine learning algorithms excel at sequence-based pattern recognition, pinpointing target variations within billions of base pairs.",
        body_style
    ))
    
    story.append(Paragraph("3.1 Sequence Alignment and Genome Annotation", h2_style))
    story.append(Paragraph(
        "Deep convolutional neural networks (CNNs) have largely optimized automated genome annotation. By treating nucleotide sequences as one-dimensional spatial text structures, CNN layers can automatically extract spatial motifs—such as splice sites, promoters, and transcription factor binding regions—without needing manually engineered feature extractions.",
        body_style
    ))
    
    story.append(Paragraph("3.2 Variant Calling and Variant Effect Prediction", h2_style))
    story.append(Paragraph(
        "Identifying single nucleotide polymorphisms (SNPs) and structural insertions/deletions is key to diagnosing genetic diseases. Supervised ML architectures classify valid biological variants versus technological sequencing errors. Models like Random Forests and Gradient Boosted Trees assess conservation scores, biochemical alterations, and genomic positions to accurately predict whether mutations are benign or pathogenic.",
        body_style
    ))
    
    story.append(PageBreak()) # Shift to Page 3

    # ==========================================
    # PAGE 3: PROTEOMICS & STRUCTURAL BIOINFORMATICS
    # ==========================================
    story.append(Paragraph("4. Structural Proteomics and Spatial Modeling", h1_style))
    story.append(Paragraph(
        "Proteins are the primary functional workhorses of biological cells. Understanding their exact three-dimensional spatial coordinates is crucial to uncovering cellular mechanisms and creating target therapeutics.",
        body_style
    ))
    
    story.append(Paragraph("4.1 Protein Structure Prediction (The AlphaFold Paradigm)", h2_style))
    story.append(Paragraph(
        "For over five decades, calculating how a one-dimensional amino acid sequence folds into a complex three-dimensional protein shape remained a grand challenge in structural biology. The development of advanced deep learning models revolutionized this pipeline. By treating protein folding as a spatial graph-transformer problem, modern architectures leverage evolutionary constraints alongside physical geometry to map spatial distances between amino acid residues with extraordinary atomic accuracy.",
        body_style
    ))
    
    # Comparative Data Table
    story.append(Spacer(1, 10))
    table_data = [
        [Paragraph("<b>Metric / Approach</b>", body_style), Paragraph("<b>Traditional Heuristics</b>", body_style), Paragraph("<b>Modern ML Paradigms</b>", body_style)],
        [Paragraph("Execution Timeline", body_style), Paragraph("Months to Years (X-ray/NMR)", body_style), Paragraph("Minutes to Hours (In-Silico Inference)", body_style)],
        [Paragraph("Scalability Scope", body_style), Paragraph("Low (One protein per run)", body_style), Paragraph("High (Whole-proteome tracking)", body_style)],
        [Paragraph("Non-linear Adaptability", body_style), Paragraph("Poor (Rigid physical constraints)", body_style), Paragraph("Excellent (Deep geometric learning)", body_style)]
    ]
    t = Table(table_data, colWidths=[150, 170, 184])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F1F5F9")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(t)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("4.2 Mass Spectrometry Data Processing", h2_style))
    story.append(Paragraph(
        "High-throughput proteomics relies on mass spectrometry to identify peptide structures. Deep recurrent networks (RNNs) and Long Short-Term Memory (LSTM) cells simulate and accurately predict peptide fragmentation patterns, significantly speeding up database cross-referencing and protein verification pipelines.",
        body_style
    ))
    
    story.append(PageBreak()) # Shift to Page 4

    # ==========================================
    # PAGE 4: DRUG DISCOVERY INTEGRATION
    # ==========================================
    story.append(Paragraph("5. AI-Driven Drug Discovery and Target Interaction", h1_style))
    story.append(Paragraph(
        "Traditional pipeline workflows for bringing a novel drug candidate to market take over a decade and cost billions of dollars. Machine learning significantly accelerates this process by executing ultra-high-throughput computational screens.",
        body_style
    ))
    
    story.append(Paragraph("5.1 Virtual Screening and Lead Optimization", h2_style))
    story.append(Paragraph(
        "Generative AI models, such as Variational Autoencoders (VAEs) and Generative Adversarial Networks (GANs), allow scientists to perform inverse molecular design. Rather than screening existing libraries manually, these models generate completely novel, synthesis-ready molecular structures tailored to bind tightly with target disease proteins.",
        body_style
    ))
    
    story.append(Paragraph("5.2 Quantitative Structure-Activity Relationship (QSAR)", h2_style))
    story.append(Paragraph(
        "Using classical regression models alongside deep neural networks, QSAR models learn to map the exact relationship between chemical properties and biological efficacy. This permits immediate, computational filtering of toxic elements long before moving to wet-lab testing environments.",
        body_style
    ))
    
    story.append(PageBreak()) # Shift to Page 5

    # ==========================================
    # PAGE 5: CHALLENGES, FUTURE & CONCLUSION
    # ==========================================
    story.append(Paragraph("6. Core Methodological Challenges", h1_style))
    story.append(Paragraph(
        "Despite its major clinical successes, machine learning in bioinformatics faces distinct structural challenges:",
        body_style
    ))
    story.append(Paragraph("* <b>Data Sparsity and High Dimensionality:</b> Biological studies often suffer from the 'curse of dimensionality,' analyzing tens of thousands of genes across only a few dozen patients.", bullet_style))
    story.append(Paragraph("* <b>The 'Black Box' Interpretability Crisis:</b> In clinical environments, understanding <i>why</i> a model predicts a tumor classification is just as critical as accuracy. Opaque deep architectures make clinical integration challenging.", bullet_style))
    story.append(Paragraph("* <b>Batch Effects and Data Heterogeneity:</b> Differences in lab equipment and sample preparation introduce non-biological variances that can mislead naive machine learning models.", bullet_style))
    
    story.append(Paragraph("7. Future Research Vectors", h1_style))
    story.append(Paragraph(
        "The future of bioinformatics relies heavily on Explainable AI (XAI) frameworks and multimodal transformers that seamlessly ingest diverse datasets—including clinical texts, imaging data, and spatial single-cell multi-omics—into unified predictive models.",
        body_style
    ))
    
    story.append(Paragraph("8. Conclusion", h1_style))
    story.append(Paragraph(
        "Machine learning has evolved from an experimental computational technique into a foundational pillar of modern biological discovery. By automating intricate pattern matching across massive datasets, ML accelerates everything from basic functional genomics to personalized medicine. Addressing algorithmic black-box interpretability will unlock next-generation precision diagnostics and therapeutic discovery.",
        body_style
    ))
    
    story.append(PageBreak()) # Shift to Page 6

    # ==========================================
    # PAGE 6: ACADEMIC REFERENCES
    # ==========================================
    story.append(Paragraph("9. Academic References", h1_style))
    
    refs = [
        "1. AlQuraishi, M. (2019). End-to-end mathematical learning of protein structure. <i>Cell Systems</i>, 8(4), 292-301.",
        "2. Jumper, J., Evans, R., Pritzel, A., et al. (2021). Highly accurate protein structure prediction with AlphaFold. <i>Nature</i>, 596(7873), 583-589.",
        "3. Libbrecht, M. W., & Noble, W. S. (2015). Machine learning applications in genetics and genomics. <i>Nature Reviews Genetics</i>, 16(6), 321-332.",
        "4. Senior, A. W., Evans, R., Jumper, J., et al. (2020). Improved protein structure prediction using potentials from deep learning. <i>Nature</i>, 577(7792), 706-710.",
        "5. Zou, J., Hussami, M., Cox, T. S., et al. (2019). A primer on deep learning in genomics. <i>Nature Genetics</i>, 51(1), 12-18."
    ]
    
    for ref in refs:
        story.append(Paragraph(ref, bullet_style))
        story.append(Spacer(1, 4))
        
    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✔️ Successfully generated publication-grade report: '{filename}'")

if __name__ == "__main__":
    build_pdf()