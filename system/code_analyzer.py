#!/usr/bin/env python3
"""
Code Analysis Engine — Phase 2
Scan codebase และเรียนรู้ patterns อัตโนมัติ

Usage:
    python system/code_analyzer.py           # Scan ทั้งหมด
    python system/code_analyzer.py --force   # Force rescan
"""
import argparse
import ast
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path


# Base paths
BASE_DIR = Path(__file__).parent.parent
PATTERNS_FILE = BASE_DIR / "ψ" / "memory" / "long-term" / "patterns" / "code_patterns_library.md"
ANTI_PATTERNS_FILE = BASE_DIR / "ψ" / "memory" / "long-term" / "patterns" / "anti_patterns_library.md"


class CodeAnalyzer(ast.NodeVisitor):
    """AST Visitor สำหรับวิเคราะห์โค้ด"""

    def __init__(self):
        self.functions = []
        self.classes = []
        self.imports = []
        self.try_blocks = []
        self.magic_numbers = []
        self.long_functions = []

    def visit_FunctionDef(self, node):
        """วิเคราะห์ function definitions"""
        name = node.name
        args = [arg.arg for arg in node.args.args]
        decorators = [d.id if hasattr(d, 'id') else str(d) for d in node.decorator_list]

        # นับบรรทัด
        if hasattr(node, 'body'):
            lines = len(node.body)
            if lines > 20:
                self.long_functions.append({
                    'name': name,
                    'lines': lines,
                    'file': None  # จะเติมทีหลัง
                })

        self.functions.append({
            'name': name,
            'args': args,
            'decorators': decorators,
            'lineno': node.lineno
        })

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """วิเคราะห์ class definitions"""
        self.classes.append({
            'name': node.name,
            'bases': [ast.unparse(base) if hasattr(ast, 'unparse') else str(base) for base in node.bases],
            'lineno': node.lineno
        })
        self.generic_visit(node)

    def visit_Import(self, node):
        """วิเคราะห์ imports"""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """วิเคราะห์ from imports"""
        module = node.module if node.module else ''
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_Try(self, node):
        """วิเคราะห์ try-except blocks"""
        handlers = []
        for h in node.handlers:
            if h.type:
                exc_type = ast.unparse(h.type) if hasattr(ast, 'unparse') else str(h.type)
            else:
                exc_type = 'Exception'
            handlers.append(exc_type)

        self.try_blocks.append({
            'handlers': handlers,
            'has_else': bool(node.orelse),
            'has_finally': bool(node.finalbody)
        })
        self.generic_visit(node)

    def visit_Constant(self, node):
        """หา magic numbers"""
        if isinstance(node.value, (int, float)) and node.value not in [0, 1, -1]:
            # ไม่นับ 0, 1, -1 (ใช้บ่อย)
            self.magic_numbers.append({
                'value': node.value,
                'lineno': node.lineno
            })
        self.generic_visit(node)


def find_code_files(project_dir):
    """หาไฟล์โค้ดทั้งหมดใน project"""
    code_files = []

    # ไฟล์ที่ไม่ต้อง scan
    exclude_dirs = {
        'node_modules', '.git', '__pycache__', 'venv', '.venv',
        'ψ', '.claude', 'dist', 'build', '.next'
    }

    for pattern in ['**/*.py', '**/*.js', '**/*.ts', '**/*.tsx']:
        for file in project_dir.glob(pattern):
            # เช็คว่าอยู่ใน exclude directory ไหม
            if any(excl in file.parts for excl in exclude_dirs):
                continue
            code_files.append(file)

    return code_files


def analyze_file(file_path):
    """วิเคราะห์ไฟล์เดียว"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Python AST
        if file_path.suffix == '.py':
            try:
                tree = ast.parse(content, filename=str(file_path))
                analyzer = CodeAnalyzer()
                analyzer.visit(tree)

                # เติม file path สำหรับ long functions
                for fn in analyzer.long_functions:
                    fn['file'] = str(file_path.relative_to(BASE_DIR))

                return {
                    'file': file_path.relative_to(BASE_DIR),
                    'functions': analyzer.functions,
                    'classes': analyzer.classes,
                    'imports': analyzer.imports,
                    'try_blocks': analyzer.try_blocks,
                    'magic_numbers': analyzer.magic_numbers,
                    'long_functions': analyzer.long_functions
                }
            except SyntaxError:
                return None

        # JavaScript/TypeScript — ใช้ regex เบื้องต้น
        else:
            return analyze_js_file(file_path, content)

    except Exception as e:
        print(f"⚠️  Error analyzing {file_path}: {e}")
        return None


def analyze_js_file(file_path, content):
    """วิเคราะห์ JS/TS ด้วย regex (เบื้องต้น)"""
    result = {
        'file': file_path.relative_to(BASE_DIR),
        'functions': [],
        'classes': [],
        'imports': [],
        'try_blocks': [],
        'magic_numbers': [],
        'long_functions': []
    }

    # Function patterns
    func_pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)\s*=>|(?:function\s*)?\([^)]*\)))'
    for match in re.finditer(func_pattern, content):
        name = match.group(1) or match.group(2)
        if name:
            result['functions'].append({'name': name, 'args': [], 'decorators': []})

    # Class patterns
    class_pattern = r'class\s+(\w+)'
    for match in re.finditer(class_pattern, content):
        result['classes'].append({'name': match.group(1), 'bases': []})

    # Import patterns
    import_pattern = r'(?:import\s+.*?from\s+["\']([^"\']+)["\']|require\(["\']([^"\']+)["\']\))'
    for match in re.finditer(import_pattern, content):
        module = match.group(1) or match.group(2)
        if module:
            result['imports'].append(module)

    # Magic numbers
    number_pattern = r'\b([2-9]\d*|[1-9]\d+\.\d+)\b'
    for match in re.finditer(number_pattern, content):
        num = float(match.group(1))
        if num not in [0, 1, -1]:
            result['magic_numbers'].append({'value': num, 'lineno': None})

    return result


def generate_patterns_report(all_results):
    """สร้างรายงาน patterns"""
    patterns = []

    # รวม functions ทั้งหมด
    all_functions = []
    for r in all_results:
        all_functions.extend(r.get('functions', []))

    # นับ naming patterns
    function_names = [f['name'] for f in all_functions]
    name_prefixes = Counter()
    for name in function_names:
        # หา prefix เช่น get_, set_, is_, has_
        match = re.match(r'^(get|set|is|has|create|update|delete|fetch|handle|process|parse|format)_', name)
        if match:
            name_prefixes[match.group(1)] += 1

    # Function naming patterns
    for prefix, count in name_prefixes.most_common():
        if count >= 3:  # พบ 3 ครั้งขึ้นไป
            patterns.append({
                'type': 'Function Naming',
                'name': f'{prefix}_* prefix',
                'frequency': count,
                'examples': [f['name'] for f in all_functions if f['name'].startswith(prefix + '_')][:3]
            })

    # Import patterns
    all_imports = []
    for r in all_results:
        all_imports.extend(r.get('imports', []))

    import_counter = Counter(all_imports)
    for imp, count in import_counter.most_common(10):
        if count >= 2:
            patterns.append({
                'type': 'Import',
                'name': imp,
                'frequency': count,
                'note': 'ใช้บ่อย'
            })

    # Try-except patterns
    all_try_blocks = []
    for r in all_results:
        all_try_blocks.extend(r.get('try_blocks', []))

    if all_try_blocks:
        exception_types = Counter()
        for tb in all_try_blocks:
            for exc in tb.get('handlers', []):
                exception_types[exc] += 1

        for exc, count in exception_types.most_common(5):
            patterns.append({
                'type': 'Error Handling',
                'name': f'except {exc}',
                'frequency': count
            })

    return patterns


def generate_anti_patterns_report(all_results):
    """สร้างรายงาน anti-patterns"""
    anti_patterns = []

    # Magic numbers
    all_magic_numbers = []
    for r in all_results:
        all_magic_numbers.extend(r.get('magic_numbers', []))

    if all_magic_numbers:
        number_counter = Counter(n['value'] for n in all_magic_numbers)
        for num, count in number_counter.most_common(10):
            if count >= 2:
                anti_patterns.append({
                    'type': 'Magic Number',
                    'name': f'Number {num}',
                    'frequency': count,
                    'severity': 'medium' if count >= 3 else 'low',
                    'suggestion': f'กำหนดเป็น constant เช่น DEFAULT_TIMEOUT = {num}'
                })

    # Long functions
    all_long_functions = []
    for r in all_results:
        all_long_functions.extend(r.get('long_functions', []))

    if all_long_functions:
        anti_patterns.append({
            'type': 'Code Smell',
            'name': 'Long Functions (> 20 lines)',
            'count': len(all_long_functions),
            'severity': 'medium',
            'examples': [f"{fn['name']} ({fn['lines']} lines)" for fn in all_long_functions[:3]]
        })

    return anti_patterns


def update_patterns_file(patterns):
    """อัปเดต code_patterns_library.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # อ่านเดิม
    if PATTERNS_FILE.exists():
        with open(PATTERNS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# Code Patterns Library\n\n## Auto-discovered Patterns\n\n"

    # เพิ่ม patterns ใหม่
    new_section = f"\n## Scan Results — {timestamp}\n\n"

    for p in patterns:
        new_section += f"### {p['type']}: {p['name']}\n\n"
        new_section += f"**ความถี่:** {p['frequency']} ครั้ง\n\n"

        if 'examples' in p:
            new_section += f"**ตัวอย่าง:**\n```python\n"
            for ex in p['examples']:
                new_section += f"  {ex}\n"
            new_section += "```\n\n"

        if 'note' in p:
            new_section += f"**หมายเหตุ:** {p['note']}\n\n"

        new_section += "---\n\n"

    # เขียน
    with open(PATTERNS_FILE, 'w', encoding='utf-8') as f:
        f.write(content + new_section)

    print(f"✅ Updated {PATTERNS_FILE.relative_to(BASE_DIR)}")


def update_anti_patterns_file(anti_patterns):
    """อัปเดต anti_patterns_library.md"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    # อ่านเดิม
    if ANTI_PATTERNS_FILE.exists():
        with open(ANTI_PATTERNS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# Anti-Patterns Library\n\n## Auto-detected Issues\n\n"

    # เพิ่ม anti-patterns ใหม่
    new_section = f"\n## Scan Results — {timestamp}\n\n"

    for ap in anti_patterns:
        severity_icon = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢'
        }.get(ap.get('severity', 'low'), '⚪')

        new_section += f"### {severity_icon} {ap['type']}: {ap['name']}\n\n"

        if 'count' in ap:
            new_section += f"**จำนวน:** {ap['count']} functions\n\n"
        else:
            new_section += f"**ความถี่:** {ap['frequency']} ครั้ง\n\n"

        if 'examples' in ap:
            new_section += f"**ตัวอย่าง:**\n"
            for ex in ap['examples']:
                new_section += f"- {ex}\n"
            new_section += "\n"

        if 'suggestion' in ap:
            new_section += f"**ควรแก้:** {ap['suggestion']}\n\n"

        new_section += "---\n\n"

    # เขียน
    with open(ANTI_PATTERNS_FILE, 'w', encoding='utf-8') as f:
        f.write(content + new_section)

    print(f"✅ Updated {ANTI_PATTERNS_FILE.relative_to(BASE_DIR)}")


def main():
    parser = argparse.ArgumentParser(
        description="Code Analysis Engine — Scan และเรียนรู้ patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--force', action='store_true', help='Force rescan (ไม่ skip)')
    parser.add_argument('--project', default=str(BASE_DIR), help='Project directory')

    args = parser.parse_args()

    project_dir = Path(args.project)

    if not project_dir.exists():
        print(f"❌ Project directory not found: {project_dir}")
        sys.exit(1)

    print(f"🔍 Scanning {project_dir}...")

    # หาไฟล์โค้ด
    code_files = find_code_files(project_dir)
    print(f"📁 Found {len(code_files)} code files")

    # วิเคราะห์
    all_results = []
    for i, file in enumerate(code_files, 1):
        print(f"  [{i}/{len(code_files)}] {file.relative_to(project_dir)}", end='\r')
        result = analyze_file(file)
        if result:
            all_results.append(result)

    print(f"\n✅ Analyzed {len(all_results)} files")

    # สร้างรายงาน
    print("\n📊 Generating reports...")

    patterns = generate_patterns_report(all_results)
    anti_patterns = generate_anti_patterns_report(all_results)

    print(f"  📌 Found {len(patterns)} patterns")
    print(f"  ⚠️  Found {len(anti_patterns)} anti-patterns")

    # อัปเดต files
    update_patterns_file(patterns)
    update_anti_patterns_file(anti_patterns)

    print("\n✨ Done!")


if __name__ == "__main__":
    main()
