const downloadBtn = document.getElementById('download');
const jsonData = document.getElementById('json-data');
const copyBtn = document.getElementById('copy');

copyBtn.addEventListener('click', () => {
    const jsonContent = jsonData.textContent;
    navigator.clipboard.writeText(jsonContent).then(() => {
        alert('JSON data copied to clipboard!');
    }).catch(err => {
        console.error('Failed to copy JSON data: ', err);
        alert('Failed to copy JSON data. Please try again.');
    });
});

downloadBtn.addEventListener('click', () => {
    const jsonContent = jsonData.textContent;
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'pharmguard-data.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});