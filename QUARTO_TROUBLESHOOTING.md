# Quarto Rendering Troubleshooting

## Python Kernel Timeout Issue

If you encounter "Kernel didn't respond in 60 seconds" errors when rendering:

### Quick Fix Option 1: Use Frozen Results Only

Update `_quarto.yml` execute section:

```yaml
execute:
  freeze: true  # Only use pre-computed results, skip execution
```

### Quick Fix Option 2: Increase Timeout

The timeout has already been increased to 300 seconds (5 minutes) in the configuration.

### Quick Fix Option 3: Pre-render Random Forest Document

Render the document separately first to create frozen outputs:

```bash
cd Quarto
quarto render randomforest.qmd
cd ..
```

Then the batch render will use the frozen outputs.

### Quick Fix Option 4: Skip Execution for Batch Builds

Temporarily disable execution for the randomforest document by adding to its YAML header:

```yaml
execute:
  freeze: true
```

Or comment it out from the render list in `_quarto.yml`.

## Testing the Fix

1. Try rendering again:

   ```bash
   ./scripts/render_gh_pages.sh
   ```

2. If still failing, use freeze mode:

   ```yaml
   # In _quarto.yml
   execute:
     freeze: true
   ```

3. Or render randomforest separately:

   ```bash
   quarto render Quarto/randomforest.qmd
   ```
