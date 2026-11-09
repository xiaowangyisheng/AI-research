"""Executable smoke tests for structural claims and non-destructive packaging."""
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from audit_svg import audit
from package_delivery import package

class HelperTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ga-skill-test-')
        self.root = Path(self.temp.name)
    def tearDown(self):
        self.temp.cleanup()
    def svg(self, body):
        p = self.root / 'figure.svg'
        p.write_text('<svg xmlns="http://www.w3.org/2000/svg">'+body+'</svg>', encoding='utf-8')
        return p
    def test_native_vectors_and_text(self):
        r = audit(self.svg('<path id="a" d="M0 0L1 1"/><text>Hello</text>'), require_text=True)
        self.assertTrue(r['structural_pass'])
        self.assertEqual(r['paths'], 1)
        self.assertEqual(r['native_text_elements'], 1)
    def test_raster_wrapper_not_full_vector(self):
        p = self.svg('<image href="data:image/png;base64,AAAA"/>')
        self.assertFalse(audit(p)['structural_pass'])
        self.assertTrue(audit(p, expect='hybrid')['structural_pass'])
        self.assertFalse(audit(p, expect='hybrid', require_text=True)['structural_pass'])
    def test_external_and_broken_refs(self):
        p = self.svg('<image href="file:///private/example.png"/><path marker-end="url(#missing)"/>')
        r = audit(p, expect='hybrid')
        self.assertFalse(r['structural_pass'])
        self.assertEqual(r['unresolved_internal_ids'], ['missing'])
    def test_duplicate_and_active_content(self):
        p = self.svg('<path id="a"/><path id="a"/><script/>')
        self.assertFalse(audit(p)['structural_pass'])
    def manifest(self, files, required):
        p = self.root / 'input_manifest.json'
        p.write_text(json.dumps({'project':'test', 'required_roles':required,'files':files}), encoding='utf-8')
        return p
    def test_background_only_package_and_no_overwrite(self):
        (self.root/'background.txt').write_text('test background asset',encoding='utf-8')
        m = self.manifest([{'path':'background.txt','role':'background'}],['background'])
        output = self.root/'package.zip'
        result = package(self.root,m,output)
        self.assertTrue(result['zip_integrity_pass'])
        with zipfile.ZipFile(output) as archive:
            info=json.loads(archive.read('delivery_manifest.json'))
            self.assertEqual(len(info['files'][0]['sha256']),64)
        before=output.read_bytes()
        with self.assertRaises(FileExistsError):package(self.root,m,output)
        self.assertEqual(before,output.read_bytes())
    def test_missing_role_and_path_escape(self):
        (self.root/'file.txt').write_text('asset',encoding='utf-8')
        m=self.manifest([{'path':'file.txt','role':'editable'}],['background'])
        with self.assertRaises(ValueError):package(self.root,m,self.root/'bad.zip')
        m=self.manifest([{'path':'../escape.txt','role':'editable'}],['editable'])
        with self.assertRaises(ValueError):package(self.root,m,self.root/'bad.zip')
        self.assertFalse((self.root/'bad.zip').exists())
    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory(prefix='ga-outside-') as outside:
            source=Path(outside)/'asset.txt';source.write_text('private',encoding='utf-8')
            (self.root/'link.txt').symlink_to(source)
            m=self.manifest([{'path':'link.txt','role':'editable'}],['editable'])
            with self.assertRaises(ValueError):package(self.root,m,self.root/'bad.zip')

if __name__ == '__main__':
    unittest.main()
