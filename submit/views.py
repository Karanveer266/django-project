from django.shortcuts import render
from submit.forms    import CodeSubmissionForm
from submit.utils    import run_code

def submit(request):
    """
    View that handles both the form display and the submission processing.
    Synchronous version (no Celery yet).
    """
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if not form.is_valid():
            return render(request, "index.html", {"form": form})

        # save basic info but defer DB write so we can add results
        submission = form.save(commit=False)

        # ---- run the user code ----
        result = run_code(
            language   = submission.language,
            code       = submission.code,
            input_data = submission.input_data or "",
        )
        # ---------------------------

        submission.status      = result["status"]
        submission.output_data = result["stdout"]
        submission.error_data  = result["stderr"]
        submission.save()

        return render(request, "result.html", {"submission": submission})

    # GET request – render empty form
    return render(request, "index.html", {"form": CodeSubmissionForm()})
