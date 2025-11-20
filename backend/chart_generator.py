try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False
    
import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  
from typing import Dict, List, Optional
import os
from backend.llm_service import LLMService

class ChartGenerator:
    """Generate charts from data files"""

    def __init__(self):
        """Initialize chart generator"""
        self.llm_service = LLMService()
        self.output_dir = 'outputs/charts'
        os.makedirs(self.output_dir, exist_ok=True)
    
    def load_data(self, file_path: str):
        """Load data from CSV or Excel file"""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.csv':
            if HAS_PANDAS:
                return pd.read_csv(file_path)
            else:
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                return data
        elif ext in ['.xlsx', '.xls']:
            if not HAS_PANDAS:
                raise ValueError("Excel files require pandas. Please install: pip install pandas openpyxl")
            
            try:
                return pd.read_excel(file_path)
            except Exception as e:
                print(f"Pandas read_excel failed: {e}. Trying fallback...")
                try:
                    import openpyxl
                    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
                    ws = wb.active
                    data = list(ws.values)
                    wb.close()
                    
                    if data:
                        cols = data[0]
                        rows = data[1:]
                        return pd.DataFrame(rows, columns=cols)
                    else:
                        return pd.DataFrame()
                except Exception as e2:
                    raise ValueError(f"Failed to read Excel file: {e} | Fallback error: {e2}")
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def infer_chart_type(self, df) -> str:
        """Infer appropriate chart type from data"""
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            num_cols = len(df.select_dtypes(include=['number']).columns)
            num_rows = len(df)
        else:
            if not df:
                return 'bar'
            num_cols = len(df[0].keys())
            num_rows = len(df)
        
        if num_cols == 1:
            return 'bar'
        elif num_cols == 2 and num_rows < 20:
            return 'scatter'
        elif num_cols >= 2 and num_rows < 10:
            return 'bar'
        elif num_cols >= 2:
            return 'line'
        else:
            return 'bar'
    
    def generate_bar_chart(self, df, output_path: str, title: str = ""):
        """Generate bar chart"""
        plt.figure(figsize=(10, 6))
        
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            if len(df.columns) >= 2:
                x_col = df.columns[0]
                y_col = df.columns[1]
                plt.bar(df[x_col], df[y_col], color='#4A90E2')
                plt.xlabel(x_col)
                plt.ylabel(y_col)
            else:
                df.plot(kind='bar', color='#4A90E2')
        else:
            if df and len(df[0].keys()) >= 2:
                keys = list(df[0].keys())
                x_data = [row[keys[0]] for row in df]
                y_data = [float(row[keys[1]]) for row in df]
                plt.bar(x_data, y_data, color='#4A90E2')
                plt.xlabel(keys[0])
                plt.ylabel(keys[1])
        
        if title:
            plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_line_chart(self, df, output_path: str, title: str = ""):
        """Generate line chart"""
        plt.figure(figsize=(10, 6))
        
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            numeric_cols = df.select_dtypes(include=['number']).columns
            for col in numeric_cols:
                plt.plot(df.index, df[col], marker='o', label=col, linewidth=2)
        else:
            if df:
                keys = list(df[0].keys())
                x_key = keys[0]
                x_data = [row[x_key] for row in df]
                
                for key in keys[1:]:
                    try:
                        y_data = [float(row[key]) for row in df]
                        plt.plot(x_data, y_data, marker='o', label=key, linewidth=2)
                    except ValueError:
                        continue
        
        if title:
            plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_scatter_chart(self, df, output_path: str, title: str = ""):
        """Generate scatter plot"""
        plt.figure(figsize=(10, 6))
        
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            if len(df.columns) >= 2:
                x_col = df.columns[0]
                y_col = df.columns[1]
                plt.scatter(df[x_col], df[y_col], color='#4A90E2', s=100, alpha=0.6)
                plt.xlabel(x_col)
                plt.ylabel(y_col)
        else:
            if df and len(df[0].keys()) >= 2:
                keys = list(df[0].keys())
                x_data = [row[keys[0]] for row in df]
                y_data = [float(row[keys[1]]) for row in df]
                plt.scatter(x_data, y_data, color='#4A90E2', s=100, alpha=0.6)
                plt.xlabel(keys[0])
                plt.ylabel(keys[1])
        
        if title:
            plt.title(title, fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_pie_chart(self, df, output_path: str, title: str = ""):
        """Generate pie chart"""
        plt.figure(figsize=(10, 6))
        
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            if len(df.columns) >= 2:
                labels = df[df.columns[0]]
                values = df[df.columns[1]]
                plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        else:
            if df and len(df[0].keys()) >= 2:
                keys = list(df[0].keys())
                labels = [row[keys[0]] for row in df]
                values = [float(row[keys[1]]) for row in df]
                plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        
        if title:
            plt.title(title, fontsize=16, fontweight='bold')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def generate_chart(self, file_path: str, chart_type: Optional[str] = None, 
                      title: str = "") -> Dict:
        """Generate chart from data file"""
        df = self.load_data(file_path)
        
        if not chart_type:
            chart_type = self.infer_chart_type(df)
        
        filename = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(self.output_dir, f"{filename}_{chart_type}.png")
        

        if chart_type == 'bar':
            self.generate_bar_chart(df, output_path, title)
        elif chart_type == 'line':
            self.generate_line_chart(df, output_path, title)
        elif chart_type == 'scatter':
            self.generate_scatter_chart(df, output_path, title)
        elif chart_type == 'pie':
            self.generate_pie_chart(df, output_path, title)
        else:
            self.generate_bar_chart(df, output_path, title)
        
        if HAS_PANDAS and isinstance(df, pd.DataFrame):
            data_summary = {
                'columns': list(df.columns),
                'row_count': len(df),
                'sample_data': df.head(3).to_dict()
            }
        else:

            if df:
                columns = list(df[0].keys())
                sample = df[:3]
                data_summary = {
                    'columns': columns,
                    'row_count': len(df),
                    'sample_data': sample
                }
            else:
                data_summary = {'columns': [], 'row_count': 0, 'sample_data': []}
                
        caption = self.llm_service.generate_chart_caption(data_summary, chart_type)
        
        return {
            'chart_path': output_path,
            'chart_type': chart_type,
            'caption': caption,
            'data_summary': data_summary
        }
    
    def generate_multiple_charts(self, file_path: str) -> List[Dict]:
        """Generate multiple chart types from same data"""
        df = self.load_data(file_path)
        charts = []
        
        chart_types = ['bar', 'line']
        for chart_type in chart_types:
            try:
                result = self.generate_chart(file_path, chart_type)
                charts.append(result)
            except Exception as e:
                print(f"Error generating {chart_type} chart: {e}")
        
        return charts
