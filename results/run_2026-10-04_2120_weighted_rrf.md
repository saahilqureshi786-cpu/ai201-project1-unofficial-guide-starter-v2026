# Run log — weighted_rrf

- Produced by: `run_eval.py::main`
- Retrieval: `store.py::search`, chunks from `chunker.py::split_documents`
- Corpus: `campus_life` (index variant `default`)
- top-k: 5 · relevance cutoff: 0.6
- Runs per question: 3, caching off
- When: 2026-10-04 21:20

This table is one row per QUESTION. The run log your README asks for is
one row per CRITERION, so aggregate these into it — criterion 1 is how many
of your questions had the answer in the retrieved chunks, and so on.

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| When do housing lottery numbers come out? | pass | pass | pass |
| How are juniors and seniors ordered in the housing lottery? | pass | pass | pass |
| How long does it usually take west lot parking permits to sell out? | pass | pass | pass |
| How far in advance should students book an adviser before registration? | pass | pass | pass |
| How much does laundry cost to wash a load at Morrow House? | pass | pass | pass |

---

## The relevance gate on out-of-corpus questions

Produced by `run_eval.py::check_out_of_scope`, cutoff 0.6. Refused 5 of 5.

Retrieval is deterministic and the gate is a comparison against a
fixed number, so these do not vary between runs — one pass over the
list is the whole measurement.

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.869 | refused |
| How do I change the oil in a diesel engine? | 0.934 | refused |
| Who won the 1994 World Cup? | 0.886 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.860 | refused |
| How do I write a for loop in Rust? | 0.900 | refused |

---

## Real output

This is what the system actually produced. Paste the relevant parts
into your README underneath the table — the rubric asks for real
output as text, not a description of it.

### When do housing lottery numbers come out? — run 1

- Best distance: 0.3453 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, admin_study_abroad.txt, advising_registration.txt, housing_morrow_house.txt

```
Housing lottery numbers come out the second week of March (admin_housing_lottery.txt).
```

### When do housing lottery numbers come out? — run 2

- Best distance: 0.3453 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, admin_study_abroad.txt, advising_registration.txt, housing_morrow_house.txt

```
Housing lottery numbers come out the second week of March (admin_housing_lottery.txt).
```

### When do housing lottery numbers come out? — run 3

- Best distance: 0.3453 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, admin_parking_permits.txt, admin_study_abroad.txt, advising_registration.txt, housing_morrow_house.txt

```
Housing lottery numbers come out the second week of March (admin_housing_lottery.txt).
```

### How are juniors and seniors ordered in the housing lottery? — run 1

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, housing_morrow_house.txt, housing_old_brewhouse.txt, housing_tamsin_court.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used if needed. (Source: admin_housing_lottery.txt)
```

### How are juniors and seniors ordered in the housing lottery? — run 2

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, housing_morrow_house.txt, housing_old_brewhouse.txt, housing_tamsin_court.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used only if needed (admin_housing_lottery.txt).
```

### How are juniors and seniors ordered in the housing lottery? — run 3

- Best distance: 0.2250 (passed the gate)
- Sources retrieved: admin_housing_lottery.txt, advising_registration.txt, housing_morrow_house.txt, housing_old_brewhouse.txt, housing_tamsin_court.txt

```
Juniors and seniors are ordered by accumulated credit hours first, with a random tie-break used only if needed (admin_housing_lottery.txt).
```

### How long does it usually take west lot parking permits to sell out? — run 1

- Best distance: 0.2264 (passed the gate)
- Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, dining_halden_hall_followup.txt, dining_verrill_street_grill_followup.txt, transit_walking.txt

```
Student permits for the west lots sell out in about three days, according to `admin_parking_permits.txt`.
```

### How long does it usually take west lot parking permits to sell out? — run 2

- Best distance: 0.2264 (passed the gate)
- Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, dining_halden_hall_followup.txt, dining_verrill_street_grill_followup.txt, transit_walking.txt

```
Student permits for the west lots sell out in about three days, according to `admin_parking_permits.txt`.
```

### How long does it usually take west lot parking permits to sell out? — run 3

- Best distance: 0.2264 (passed the gate)
- Sources retrieved: admin_library_holds.txt, admin_parking_permits.txt, dining_halden_hall_followup.txt, dining_verrill_street_grill_followup.txt, transit_walking.txt

```
Student permits for the west lots sell out in about three days, according to `admin_parking_permits.txt`.
```

### How far in advance should students book an adviser before registration? — run 1

- Best distance: 0.3586 (passed the gate)
- Sources retrieved: admin_declaring_a_major.txt, admin_library_holds.txt, advising_registration.txt, course_cs_340.txt, dining_verrill_street_grill_followup.txt

```
Students should book an adviser two weeks in advance. This information comes from advising_registration.txt.
```

### How far in advance should students book an adviser before registration? — run 2

- Best distance: 0.3586 (passed the gate)
- Sources retrieved: admin_declaring_a_major.txt, admin_library_holds.txt, advising_registration.txt, course_cs_340.txt, dining_verrill_street_grill_followup.txt

```
Students should book an adviser two weeks out, as advisers get busy in the week before registration opens. 

Source: advising_registration.txt
```

### How far in advance should students book an adviser before registration? — run 3

- Best distance: 0.3586 (passed the gate)
- Sources retrieved: admin_declaring_a_major.txt, admin_library_holds.txt, advising_registration.txt, course_cs_340.txt, dining_verrill_street_grill_followup.txt

```
Students should book an adviser two weeks in advance. 

Source: advising_registration.txt
```

### How much does laundry cost to wash a load at Morrow House? — run 1

- Best distance: 0.2041 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_morrow_house_noise.txt

```
Laundry costs $1.50 to wash a load at Morrow House. This information comes from `housing_morrow_house_laundry.txt` and `housing_morrow_house.txt`.
```

### How much does laundry cost to wash a load at Morrow House? — run 2

- Best distance: 0.2041 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_morrow_house_noise.txt

```
At Morrow House, a wash costs $1.50. This information comes from `housing_morrow_house_laundry.txt` and `housing_morrow_house.txt`.
```

### How much does laundry cost to wash a load at Morrow House? — run 3

- Best distance: 0.2041 (passed the gate)
- Sources retrieved: housing_aldridge_hall_laundry.txt, housing_innisfree_hall_laundry.txt, housing_morrow_house.txt, housing_morrow_house_laundry.txt, housing_morrow_house_noise.txt

```
Laundry costs $1.50 to wash a load at Morrow House. This is from `housing_morrow_house.txt` and `housing_morrow_house_laundry.txt`.
```
