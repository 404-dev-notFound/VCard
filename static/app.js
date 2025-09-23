// Sample data for demonstration
const sampleData = {
  businessCard: {
    first_name: "Dev",
    middle_name: "D",
    last_name: "Yadav", 
    company_name: "ODeX Global",
    position: "Software Engineer",
    department: "Engineering",
    mobile: "+1234567890",
    telephone: "+1987654321",
    email: "dev.yadav@odexglobal.com",
    address: "123 Innovation Drive, Silicon Valley, CA 94000",
    extension: "405",
    website: "https://odexglobal.com",
    notes: "Specializes in AI/ML solutions and cloud architecture"
  },
  rawText: "Dev D. Yadav\nSoftware Engineer\nODeX Global\nEngineering Department\n\nMobile: +1 (234) 567-8900\nOffice: +1 (987) 654-3210 ext. 405\nEmail: dev.yadav@odexglobal.com\nWeb: https://odexglobal.com\n\n123 Innovation Drive\nSilicon Valley, CA 94000\n\nSpecializes in AI/ML solutions\nand cloud architecture",
  vCard: "BEGIN:VCARD\nVERSION:3.0\nN:Yadav;Dev;D;;\nFN:Dev D Yadav\nORG:ODeX Global\nTITLE:Software Engineer\nX-DEPARTMENT:Engineering\nTEL;TYPE=CELL:+1234567890\nTEL;TYPE=WORK:+1987654321\nX-EXTENSION:405\nEMAIL;TYPE=WORK:dev.yadav@odexglobal.com\nADR;TYPE=WORK:;;123 Innovation Drive, Silicon Valley, CA 94000;;;;\nURL:https://odexglobal.com\nNOTE:Specializes in AI/ML solutions and cloud architecture\nREV:20250822T040649Z\nEND:VCARD"
};

class BusinessCardOCR {
  constructor() {
    this.initializeElements();
    this.attachEventListeners();
    this.sessionId = self.crypto.randomUUID();
  }

  initializeElements() {
    this.uploadArea = document.getElementById('uploadArea');
    this.fileInput = document.getElementById('fileInput');
    this.fileInfo = document.getElementById('fileInfo');
    this.fileName = document.getElementById('fileName');
    this.fileSize = document.getElementById('fileSize');
    this.processBtn = document.getElementById('processBtn');
    this.demoBtn = document.getElementById('demoBtn');
    this.uploadSection = document.getElementById('uploadSection');
    this.processingSection = document.getElementById('processingSection');
    this.resultsSection = document.getElementById('resultsSection');
    this.processingStep = document.getElementById('processingStep');
    this.progressFill = document.getElementById('progressFill');
    this.dataGrid = document.getElementById('dataGrid');
    this.vcardOutput = document.getElementById('vcardOutput');
    this.rawText = document.getElementById('rawText');
    this.downloadBtn = document.getElementById('downloadBtn');
    this.resetBtn = document.getElementById('resetBtn');
    this.tabBtns = document.querySelectorAll('.tab-btn');
    this.tabPanels = document.querySelectorAll('.tab-panel');
    this.exportBtn = document.getElementById('exportBtn');
  }

  attachEventListeners() {
    this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
    this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
    this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
    this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
    this.processBtn.addEventListener('click', () => this.processImage());
    this.demoBtn.addEventListener('click', () => this.runDemo());
    this.downloadBtn.addEventListener('click', () => this.downloadVCard());
    this.resetBtn.addEventListener('click', () => this.reset());
    this.exportBtn.addEventListener('click', () => this.exportCSV());
    this.tabBtns.forEach(btn => {
      btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
    });
  }

  handleDragOver(e) { e.preventDefault(); this.uploadArea.classList.add('dragover'); }
  handleDragLeave(e) { e.preventDefault(); this.uploadArea.classList.remove('dragover'); }

  handleDrop(e) {
    e.preventDefault();
    this.uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) this.handleFiles(files);
  }

  handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) this.handleFiles(files);
  }

  // ✅ MODIFIED: Handles 1 or 2 files
  handleFiles(files) {
    this.fileInput.files = files; 

    if (files.length < 1 || files.length > 2) {
      alert('Please select 1 or 2 image files (for front and back).');
      this.fileName.textContent = `${files.length} file(s) selected. (1 or 2 required)`;
      this.fileSize.textContent = '';
      this.fileInfo.classList.remove('hidden');
      return;
    }

    let totalSize = 0;
    for (const file of files) {
      if (!file.type.startsWith('image/')) {
        alert('Please select only image files.');
        return;
      }
      totalSize += file.size;
    }
    
    this.fileName.textContent = `${files.length} file(s) selected`;
    this.fileSize.textContent = `Total size: ${this.formatFileSize(totalSize)}`;
    this.fileInfo.classList.remove('hidden');
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }

  // ✅ MODIFIED: Validates for 1 or 2 files before sending
  async processImage() {
    const files = this.fileInput.files;

    if (files.length < 1 || files.length > 2) {
      alert('Please select 1 or 2 images to process.');
      return;
    }
    this.showProcessingAnimation();

    const formData = new FormData();
    for (const file of files) {
      formData.append('files', file);
    }
    formData.append('include_vcard', 'true');
    formData.append('include_raw_text', 'true');
    formData.append('session_id', this.sessionId);

    try {
      const response = await fetch('/process-cards', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Failed to process images');
      }
      // The backend now sends a single result object, not an array
      const result = await response.json();
      this.showResults(result);
    } catch (error) {
      alert('Error processing images: ' + error.message);
    }
  }

  runDemo() { alert("Demo mode is disabled. Please upload an image."); }
  showProcessingAnimation() {
    // ... (this function remains the same)
    this.uploadSection.classList.add('hidden');
    this.resultsSection.classList.add('hidden');
    this.processingSection.classList.remove('hidden');
    this.processingSection.classList.add('fade-in');
    this.progressFill.style.width = '0%';
  }
  
  // ✅ MODIFIED: Handles a SINGLE result object
  showResults(result) {
    this.processingSection.classList.add('hidden');
    this.resultsSection.classList.remove('hidden');
    this.resultsSection.classList.add('fade-in');

    if (!result || !result.success || !result.structured_data) {
      alert(result.error_message || 'No structured data extracted from the image.');
      this.reset();
      return;
    }
    this.exportBtn.classList.remove('hidden');

    this.populateStructuredData(result.structured_data);
    this.populateVCard(result.vcard || '');
    this.populateRawText(result.raw_text || '');
    this.switchTab('structured');
  }

  // ✅ MODIFIED: Simplified to display just one card's data
  populateStructuredData(data) {
    const fieldLabels = {
      first_name: 'First Name', middle_name: 'Middle Name', last_name: 'Last Name',
      company_name: 'Company', position: 'Position', department: 'Department',
      mobile: 'Mobile Phone', telephone: 'Office Phone', extension: 'Extension',
      email: 'Email', website: 'Website', address: 'Address', notes: 'Additional Notes'
    };

    this.dataGrid.innerHTML = ''; 

    Object.entries(fieldLabels).forEach(([key, label]) => {
      let value = data[key];
      
      // ✅ NEW: Check if the value is an array and join it into a string
      if (Array.isArray(value)) {
        value = value.join(', ');
      }
      
      const displayValue = value || 'Not detected';
      const dataItem = document.createElement('div');
      dataItem.className = 'data-item';
      dataItem.innerHTML = `
        <div class="data-label">${label}</div>
        <div class="data-value ${displayValue === 'Not detected' ? 'empty' : ''}">${displayValue}</div>
      `;
      this.dataGrid.appendChild(dataItem);
    });
  }

  // ... (The rest of the functions: populateVCard, populateRawText, switchTab, downloadVCard, reset, etc. remain the same)
  populateVCard(vcard) { this.vcardOutput.textContent = vcard; }
  populateRawText(text) { this.rawText.textContent = text; }
  switchTab(tabName) {
    this.tabBtns.forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    this.tabPanels.forEach(panel => {
      panel.classList.toggle('active', panel.id === tabName);
    });
  }

  // ✅ NEW: Function to handle the CSV export
  async exportCSV() {
    try {
      const formData = new FormData();
      formData.append('session_id', this.sessionId);

      const response = await fetch('/export-csv', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to export CSV.');
      }

      // Handle the file download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      // Extract filename from response headers if available, otherwise use a default
      const disposition = response.headers.get('content-disposition');
      let filename = 'business_cards.csv';
      if (disposition && disposition.indexOf('attachment') !== -1) {
          const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
          const matches = filenameRegex.exec(disposition);
          if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '');
          }
      }
      a.download = filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      // Hide the button again since the session data is now cleared
      this.exportBtn.classList.add('hidden');
      alert('CSV exported successfully! Session data has been cleared.');

    } catch (error) {
      alert('Error exporting CSV: ' + error.message);
    }
  }

  downloadVCard() {
    const vcardContent = this.vcardOutput.textContent;
    const blob = new Blob([vcardContent], { type: 'text/vcard' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'contact.vcf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
  reset() {
    this.processingSection.classList.add('hidden');
    this.resultsSection.classList.add('hidden');
    this.uploadSection.classList.remove('hidden');
    this.fileInfo.classList.add('hidden');
    this.fileInput.value = '';
    this.progressFill.style.width = '0%';
    this.dataGrid.innerHTML = '';
    this.vcardOutput.textContent = '';
    this.rawText.textContent = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

document.addEventListener('DOMContentLoaded', () => { new BusinessCardOCR(); });
document.addEventListener('dragover', (e) => e.preventDefault());
document.addEventListener('drop', (e) => e.preventDefault());