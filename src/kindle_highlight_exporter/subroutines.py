def get_loc_values(loc_str):
    if "-" in loc_str:
        start = loc_str.split("-")[0]
        end = loc_str.split("-")[1]
        return int(start), int(end)
    else:
        return int(loc_str), int(loc_str)


def parse_one_clipping(clip):
    """
    Attempt to parse out relevant data for one clipping

    Parameters
    ----------
    clip : str
        Mess of metadata about book/article/etc.

    Returns
    -------
    dict
        Data dict of relevant info from clipping
    """
    clip_dict = dict()
    lines = clip.split("\n")
    clip_dict["source_title"] = lines[0].rsplit("(", 1)[0].strip()

    # Author
    try:
        clip_dict["author"] = lines[0].rsplit("(")[-1].rsplit(")")[0]
        # This indicates that something went wrong getting author:
        if clip_dict["author"] == clip_dict["source_title"]:
            clip_dict["author"] = None
    except IndexError:
        # Title and author are not obvious/separate
        clip_dict["author"] = None

    # !TODO clip_dict['datetime'] = # SOMETHING

    # Page / Location
    try:
        location_str = lines[1].split("Location ")[1].split(" |")[0]
        clip_dict["loc_start"], clip_dict["loc_end"] = get_loc_values(
            location_str
        )
    except IndexError:
        # This uses pages and not loc?
        try:
            clip_dict["page_num"] = lines[1].split("page ")[1].split(" |")[0]
        except IndexError:
            breakpoint()

    clip_dict["highlight_text"] = lines[3]
    return clip_dict


def import_kindle_textfile(file_loc):
    """
    Loads a text file from kindle "my clippings"

    Parameters
    ----------
    file_loc : str
        What is the filepath/filename of my clippings?

    Returns
    -------
    list[dict]
        List of dictionaries representing individual clippings
    """
    with open(file_loc, "r") as infile:
        all_clippings = infile.read()
    split_by_ufeff = all_clippings.split("\ufeff")
    clippings = [clip for clip in split_by_ufeff if clip]
    unsplit_last_one = clippings.pop()
    clippings.extend(unsplit_last_one.split("\n==========\n"))
    clippings = [clip for clip in clippings if clip]
    clip_dicts = [parse_one_clipping(clip) for clip in clippings]
    return clip_dicts


def get_clippings_by_author(
    clip_dicts,
    only_these_authors=None,
    exclude_these_authors=None,
):
    return get_clippings_by_field(
        clip_dicts,
        field="author",
        only_these=only_these_authors,
        exclude_these=exclude_these_authors,
    )


def get_clippings_by_field(
    clip_dicts,
    field,
    only_these=None,
    exclude_these=None,
):
    """
    Given a filter field, find relevant clips

    Parameters
    ----------
    clip_dicts : list
        clip dicts to search thru
    only_these : str or list[str], optional
        Which things we want clips for, by default None
    exclude_these : str or list[str], optional
        Which things to exclude from results, by default None

    Returns
    -------
    list[dict]
        list of clippings that match criteria
    """
    # Inclusive approach
    if only_these:
        clip_dicts = [clip for clip in clip_dicts if clip[field] in only_these]

    # Exclusive approach
    if exclude_these:
        clip_dicts = [
            clip for clip in clip_dicts if clip[field] not in exclude_these
        ]
    return clip_dicts
