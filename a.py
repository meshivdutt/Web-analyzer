import tkinter as tk
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


class WebAnalyzer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sana ka Project")
        self.root.geometry("500x500")
        self.root.resizable(width=False, height=False)

        # URL input field
        self.url_label = tk.Label(self.root, text="Enter URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self.root, width=50)
        self.url_entry.pack()

        # Buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()
        self.analyze_button = tk.Button(self.button_frame, text="Analyze", width=10, command=self.analyze)
        self.analyze_button.pack(side="left")
        self.clear_button = tk.Button(self.button_frame, text="Clear", width=10, command=self.clear)
        self.clear_button.pack(side="left")

        # Report text field
        self.report_label = tk.Label(self.root, text="Report:")
        self.report_label.pack()
        self.report_text = tk.Text(self.root, height=20, width=70)
        self.report_text.pack()

    def run(self):
        self.root.mainloop()

    def analyze(self):
        url = self.url_entry.get().strip()
        if url:
            if not url.startswith("http"):
                url = "http://" + url
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                title = soup.title.string.strip()
                links = soup.find_all('a')
                num_links = len(links)
                num_external_links = 0
                for link in links:
                    if 'http' in link.get('href'):
                        if urlparse(link.get('href')).netloc != urlparse(url).netloc:
                            num_external_links += 1
                report = f"Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                report += f"URL: {url}\n"
                report += f"Title: {title}\n"
                report += f"Number of links: {num_links}\n"
                report += f"Number of external links: {num_external_links}\n"
                report += f"Number of Paragraphs: {num_paragraphs}\n"
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(tk.END, report)
            except requests.exceptions.RequestException as e:
                self.report_text.delete(1.0, tk.END)
                self.report_text.insert(tk.END, f"Error: {str(e)}")
        else:
            self.report_text.delete(1.0, tk.END)
            self.report_text.insert(tk.END, "Please enter a URL to analyze.")

    def clear(self):
        self.url_entry.delete(0, tk.END)
        self.report_text.delete(1.0, tk.END)


if __name__ == '__main__':
    analyzer = WebAnalyzer()
    analyzer.run()
