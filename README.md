# Credit Card Benefits Tracker

This Streamlit app helps track recurring credit card benefits. It can be run locally or inside Docker.

## Configuring the data file

The application reads and writes benefit information to a JSON file. By default it uses `credit_card_benefits.json` in the working directory. You can override this location by setting the `BENEFITS_DATA_FILE` environment variable.

### Example Docker usage

Build the image:

```bash
docker build -t cc-benefits .
```

Run the container while specifying a custom data file:

```bash
docker run -p 8501:8501 \
  -e BENEFITS_DATA_FILE=/app/data/benefits.json \
  cc-benefits
```

If the variable is not set, the default file path will be used.
