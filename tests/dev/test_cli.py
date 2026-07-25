import argparse
from tradiba.dev.cli.new import handle_new
from tradiba.dev.cli.doctor import handle_doctor
from tradiba.dev.cli.validate import handle_validate
from tradiba.dev.cli.benchmark import handle_benchmark
from tradiba.dev.cli.release import handle_release

def test_new_command(tmp_path):
    args = argparse.Namespace(type="strategy", name=str(tmp_path / "my_strategy"))
    handle_new(args)
    assert (tmp_path / "my_strategy" / "__init__.py").exists()

def test_doctor_command(capsys):
    args = argparse.Namespace()
    handle_doctor(args)
    captured = capsys.readouterr()
    assert "Running Tradiba Environment Diagnostics" in captured.out
    assert "Diagnostic complete" in captured.out

def test_validate_command(capsys):
    args = argparse.Namespace(target="all")
    handle_validate(args)
    captured = capsys.readouterr()
    assert "Validating all plugins and schemas" in captured.out

def test_benchmark_command(capsys):
    args = argparse.Namespace(target="latency")
    handle_benchmark(args)
    captured = capsys.readouterr()
    assert "Running benchmarks for target: latency" in captured.out

def test_release_command(capsys):
    args = argparse.Namespace(version="2.0.0")
    handle_release(args)
    captured = capsys.readouterr()
    assert "Preparing Tradiba platform release: v2.0.0" in captured.out
